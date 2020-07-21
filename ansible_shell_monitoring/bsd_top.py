#!/usr/local/etc/ansible/venv/top/bin/python

import json,os,psycopg2,time,subprocess,yaml
from datetime import datetime

playbook_file = '/usr/local/etc/ansible/playbooks/tops.yml'


def letter_degree(value = ''):
    if value[-2].isdigit():
        if value[-1] == 'K':
            float_value = int(value[:-1])*1E3
        elif value[-1] == 'M':
            float_value = int(value[:-1])*1E6
        elif value[-1] == 'G':
            float_value = int(value[:-1])*1E9
        elif value[-1] == '%':
            float_value = int(value[:-1])
    else:
        float_value = 0
    return float_value

def get_param_id(param_name='', param_dict=''):
    for i in param_dict:
        if i[0] == param_name:
            return i[1]

def get_params_dict():
    conn = psycopg2.connect("dbname=sys_db user=postgres host=192.168.1.203")
    cur = conn.cursor()
    cur.execute("SELECT param_name, param_id FROM bsd_stat.parameters;")
    param_dict = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return param_dict

def send_parameters(vals = {}):
    conn = psycopg2.connect("dbname = sys_db user = postgres host=192.168.1.203")
    cur = conn.cursor()
    cur.execute("select param_name from bsd_stat.parameters;")
    sql_param_names = cur.fetchall()
    conn.commit()
    spn = {}
    for pname in sql_param_names:
        spn[pname[0]] = ''

    for param_key in vals.keys():
        if param_key not in spn:
            try:
                cur.execute("INSERT INTO bsd_stat.parameters (param_name) VALUES (%s);",(param_key,))
                conn.commit()
            except:
                pass
    cur.close()
    conn.close()

def send_hostname(hostname=''):
    conn = psycopg2.connect("dbname=sys_db user=postgres host=192.168.1.203")
    cur = conn.cursor()

    cur.execute("SELECT host_id FROM bsd_stat.ansible_hosts where host_name=%s",(hostname,))
    host_id = cur.fetchone()
    conn.commit()

    if host_id == None:
        try:
            cur.execute("INSERT INTO bsd_stat.ansible_hosts(host_name)  VALUES (%s);",(hostname,))
        except:
            pass
        conn.commit()
        cur.execute("SELECT host_id FROM bsd_stat.ansible_hosts where host_name=%s",(hostname,))
        host_id = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()



    return host_id

def send_values(vals = {}, param_dict = [], current_epoch_time = 0, host_id = 0):
    conn = psycopg2.connect("dbname=sys_db user=postgres host=192.168.1.203")
    cur = conn.cursor()
    for  key in vals.keys():
        param_id = get_param_id(param_name=key, param_dict = param_dict)
        try:
            cur.execute("INSERT INTO bsd_stat.top_values(param_id, param_value, epochtime, ansible_host_id)VALUES (%s,%s,%s,%s);",(param_id, vals[key], current_epoch_time, host_id))
            conn.commit()
        except:
            conn.rollback()
            pass
    cur.close()
    conn.close()

def get_file_list(top_playbook_file = 'top.yml'):
    with open(top_playbook_file) as f:
        file_list = {}
        yml = (yaml.safe_load(f))
        for i in yml:
            if os.name == 'nt':
                file_list[i['hosts']] = i['tasks'][1]['local_action']['dest'].split('/')[-1]
            else:
                file_list[i['hosts']] = i['tasks'][1]['local_action']['dest']
        return file_list


def get_sys_pid_info_from_json(lines = {}): 
    last_pid_pos = 0
    pid_list_pos = 0
    i = 0
    for line_str in lines:
        i += 1
        if line_str.startswith('last pid:') == True:
            last_pid_pos = i
        if line_str.find('PID') > 0:
            pid_list_pos = i

    last_page_processes_list = []
    for pid_params in lines[pid_list_pos-1:pid_list_pos][0].split(' '):
        if len(pid_params) > 0:
            last_page_processes_list.append(pid_params)

    last_page_top = lines[last_pid_pos-1:pid_list_pos-2]
    last_page_processes = lines[pid_list_pos:]

    return last_page_top, last_page_processes, last_page_processes_list

def get_values_from_pid_info(pid_list = [], pid = ''):
    pid_dict = {}
    for i in pid:
        pid_current_row = []
        for m in i.split(' '):
            if len(m)>0:
                pid_current_row.append(m)
        pl={}
        for j in range(len(pid_list)):
            pl[pid_list[j]] = pid_current_row[j]  
        pid_dict[pid_current_row[0]] = pl
    return pid_dict

def get_arc_parameters(sys = []):
    counter = 0
    top_dict = {}
    remove_keys = []
    for i in sys:
        top_dict[counter] = i
        counter += 1
    for i in top_dict.keys():
        if top_dict[i].find('pid:') >= 0 or top_dict[i].find('processes:') >= 0 or top_dict[i].find('CPU:') >= 0 or top_dict[i].find('Mem:') >= 0 or top_dict[i].find('Swap:') >= 0 :
            remove_keys.append(i)
    for i in remove_keys:
        top_dict.pop(i)
    ret =''
    for i in top_dict.keys():
        ret += top_dict[i]+','
    arc_dict = {}
    for i in ret.split(':',1)[1].split(','):
        if len(i)>0:
            arc_dict['arc_'+i.strip().split(' ')[1].lower()]=i.strip().split(' ')[0]
    for i in arc_dict.keys():
        if i == 'arc_ratio':
            arc_dict[i] = float(arc_dict[i].split(':')[0])/float(arc_dict[i].split(':')[1])
        else:
            arc_dict[i] = letter_degree(value = arc_dict[i])

    return arc_dict

def get_cpu_mem_swap_parameters(sys = []):
        counter = 0
        top_dict = {}
        new_vals_cpu = {}
        new_vals_mem = {}
        new_vals_swap = {}
        vals = {}
        for i in sys:
            top_dict[counter] = i
            counter += 1
        for i in top_dict.keys():
            if top_dict[i].find('CPU:') >= 0:
                if len(top_dict[i].split(':')[1].split(',')) > 1:
                    for j in top_dict[i].split(':')[1].split(','):
                        new_vals_cpu['cpu_'+j.split('%')[1].strip()] = float(j.split('%')[0].strip())
            elif top_dict[i].find('Mem:') >= 0:
                if len(top_dict[i].split(':')[1].split(',')) > 1:
                    for j in top_dict[i].split(':')[1].split(','):
                        new_vals_mem['mem_'+j.split(' ')[-1].lower()] = letter_degree(value = j.split(' ')[-2])
            elif top_dict[i].find('Swap:') >= 0 :
                if len(top_dict[i].split(':')[1].split(',')) > 1:
                    for j in top_dict[i].split(':')[1].split(','):
                        new_vals_swap['swap_'+j.split(' ')[-1].lower()] = letter_degree(value = j.split(' ')[-2])
        vals.update(new_vals_cpu)
        vals.update(new_vals_mem)
        vals.update(new_vals_swap)
        return vals

def get_load_parameters(sys = []):
        vals = {}
        begin = sys[0].split(';')[1].find(':')+1
        end = sys[0].split(';')[1].find('up')
        load_list = sys[0].split(';')[1][begin:end].replace(' ','').split(',')
        vals['load_avg_5min'] = float(load_list[0])
        vals['load_avg_10min'] = float(load_list[1])
        vals['load_avg_15min'] = float(load_list[2])
        return vals

def get_processes_params(sys = []):
    vals[sys[1].split(':')[0].split(' ')[1]]=int(sys[1].split(':')[0].split(' ')[0])
    for l in sys[1].split(':')[1].split(','):
        vals['processes_'+l.split(' ')[-1]] = int(l.split(' ')[-2])
    return vals


subprocess.call('ansible-playbook ' + playbook_file, shell=True)

vals={}

fl = get_file_list(top_playbook_file = playbook_file)


for top_file_keys in fl.keys():
    with open(fl[top_file_keys], "r") as top_file:
        json_top = json.load(top_file)
        sys,pid,pid_list = get_sys_pid_info_from_json(lines = json_top['stdout_lines'])

    try:
        vals.update(get_load_parameters(sys = sys))
    except:
        pass
    try:
        vals.update(get_processes_params(sys = sys))
    except:
        pass
    try:
        vals.update(get_cpu_mem_swap_parameters(sys = sys))
    except:
        pass
    try:
        vals.update(get_arc_parameters(sys = sys))
    except:
        pass

    current_epoch_time = int(datetime.strptime(json_top['start'], '%Y-%m-%d %H:%M:%S.%f').timestamp())
    host_id = send_hostname(hostname = top_file_keys)
    send_parameters(vals = vals)
    param_dict = get_params_dict()
    send_values(vals = vals, param_dict = param_dict, current_epoch_time = current_epoch_time, host_id = host_id)





