-- Table: bsd_stat.ansible_hosts

-- DROP TABLE bsd_stat.ansible_hosts;

CREATE TABLE bsd_stat.ansible_hosts
(
    host_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    host_name character varying(250) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT hosts_pkey PRIMARY KEY (host_id),
    CONSTRAINT ansible_hosts_host_name_key UNIQUE (host_name)
)

TABLESPACE pg_default;

ALTER TABLE bsd_stat.ansible_hosts
    OWNER to postgres;