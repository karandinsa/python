#!/usr/local/etc/ansible/venv/top/bin/python

import json,os,psycopg2,time,subprocess,yaml
from datetime import datetime

playbook_file = '/usr/local/etc/ansible/playbooks/netstat.yml'

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


def send_interfaces(name='', network='', address='', host_id=5):
    conn = psycopg2.connect("dbname=sys_db user=postgres host=192.168.1.203")
    cur = conn.cursor()
    cur.execute("SELECT interface_id FROM bsd_stat.interfaces WHERE name=%s AND network=%s AND address=%s AND host_id=%s",(name, network, address, host_id))
    interface_id = cur.fetchone()
    conn.commit()
    if interface_id == None:
        try:
            cur.execute("INSERT INTO bsd_stat.interfaces(name,network,address,host_id)  VALUES (%s,%s,%s,%s);",(name, network, address, host_id))
        except:
            pass
        conn.commit()
        cur.execute("SELECT interface_id FROM bsd_stat.interfaces WHERE name=%s AND network=%s AND address=%s AND host_id=%s",(name, network, address, host_id))
        interface_id = cur.fetchone()
        conn.commit()
    cur.close()
    conn.close()
    return interface_id

def get_param_id(param_name='', param_dict=''):
    for i in param_dict:
        if i[0] == param_name:
            return i[1]


subprocess.call('ansible-playbook ' + playbook_file, shell=True)
vals={}
fl = get_file_list(top_playbook_file = playbook_file)

for top_file_keys in fl.keys():
    with open(fl[top_file_keys], "r") as top_file:
        json_top = json.load(top_file)
        current_epoch_time = int(datetime.strptime(json_top['start'], '%Y-%m-%d %H:%M:%S.%f').timestamp())
        host_id = send_hostname(hostname = top_file_keys) 
        keys = [i for i in json_top['stdout_lines'][0].split(' ') if i !='']

        for val_strings in range(1,len(json_top['stdout_lines'])):
            values = [i for i in json_top['stdout_lines'][val_strings].split(' ') if i !='']
            ready_dict = dict(zip(keys,values))

            interface_id = send_interfaces(name = ready_dict['Name'], network = ready_dict['Network'], address = ready_dict['Address'], host_id = host_id[0])
            if_id = interface_id[0]
            interfaces_keys = ['Name','Network','Address']

            parameters_keys = [i for i in ready_dict.keys() if i not in interfaces_keys]
            for i in parameters_keys:
                vals[i]=''
            send_parameters(vals = vals)
            param_dict = get_params_dict()
            conn = psycopg2.connect("dbname=sys_db user=postgres host=192.168.1.203")
            cur = conn.cursor()
            for param_name in ready_dict.keys():
                if param_name not in interfaces_keys:
                    param_id = get_param_id(param_name = param_name, param_dict = param_dict)
                    param_value = ready_dict[param_name].replace('-','0')
                    try:
                        cur.execute("INSERT INTO bsd_stat.netstat_values(param_id, interface_id, param_value, epochtime) VALUES (%s, %s, %s, %s);",(param_id, if_id, param_value, current_epoch_time))
                        conn.commit()
                    except:
                        conn.rollback()
                        pass
            cur.close()
            conn.close()
