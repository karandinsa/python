-- Table: bsd_stat.parameters_groups

-- DROP TABLE bsd_stat.parameters_groups;

CREATE TABLE bsd_stat.parameters_groups
(
    parameter_group_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    parameter_group_name character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT parameters_groups_pkey PRIMARY KEY (parameter_group_id)
)

TABLESPACE pg_default;

ALTER TABLE bsd_stat.parameters_groups
    OWNER to postgres;