-- View: bsd_stat.top_list

-- DROP VIEW bsd_stat.top_list;

CREATE OR REPLACE VIEW bsd_stat.top_list
 AS
 SELECT top_values.top_id,
    top_values.param_id,
    top_values.param_value,
    top_values.epochtime,
    ansible_hosts.host_id,
    parameters.param_name,
    ansible_hosts.host_name,
    parameters.parameter_group_id,
    parameters_groups.parameter_group_name
   FROM bsd_stat.top_values
     LEFT JOIN bsd_stat.parameters ON top_values.param_id = parameters.param_id
     LEFT JOIN bsd_stat.ansible_hosts ON top_values.ansible_host_id = ansible_hosts.host_id
     LEFT JOIN bsd_stat.parameters_groups ON parameters_groups.parameter_group_id = parameters.parameter_group_id;

ALTER TABLE bsd_stat.top_list
    OWNER TO postgres;

