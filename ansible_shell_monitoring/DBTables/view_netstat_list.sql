-- View: bsd_stat.netstat_list

-- DROP VIEW bsd_stat.netstat_list;

CREATE OR REPLACE VIEW bsd_stat.netstat_list
 AS
 SELECT netstat_values.netstat_id,
    netstat_values.param_id,
    netstat_values.interface_id,
    netstat_values.param_value,
    netstat_values.epochtime,
    parameters.param_name,
    parameters.parameter_group_id,
    parameters_groups.parameter_group_name,
    interfaces.name,
    interfaces.network,
    interfaces.address,
    interfaces.host_id,
    ansible_hosts.host_name
   FROM bsd_stat.netstat_values
     LEFT JOIN bsd_stat.parameters ON parameters.param_id = netstat_values.param_id
     LEFT JOIN bsd_stat.parameters_groups ON parameters_groups.parameter_group_id = parameters.parameter_group_id
     LEFT JOIN bsd_stat.interfaces ON interfaces.interface_id = netstat_values.interface_id
     LEFT JOIN bsd_stat.ansible_hosts ON ansible_hosts.host_id = interfaces.host_id;

ALTER TABLE bsd_stat.netstat_list
    OWNER TO postgres;

