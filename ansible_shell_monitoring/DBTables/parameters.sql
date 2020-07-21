-- Table: bsd_stat.parameters

-- DROP TABLE bsd_stat.parameters;

CREATE TABLE bsd_stat.parameters
(
    param_name character varying(250) COLLATE pg_catalog."default" NOT NULL,
    param_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    parameter_group_id bigint NOT NULL DEFAULT 1,
    CONSTRAINT param_id PRIMARY KEY (param_id),
    CONSTRAINT param_name UNIQUE (param_name),
    CONSTRAINT parameters_groups FOREIGN KEY (parameter_group_id)
        REFERENCES bsd_stat.parameters_groups (parameter_group_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE bsd_stat.parameters
    OWNER to postgres;