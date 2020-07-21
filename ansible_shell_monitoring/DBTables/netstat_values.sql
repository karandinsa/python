-- Table: bsd_stat.netstat_values

-- DROP TABLE bsd_stat.netstat_values;

CREATE TABLE bsd_stat.netstat_values
(
    netstat_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    param_id bigint NOT NULL DEFAULT 32,
    interface_id bigint NOT NULL,
    param_value numeric(26,6) NOT NULL,
    epochtime bigint NOT NULL DEFAULT 0,
    CONSTRAINT netstat_values_pkey PRIMARY KEY (netstat_id),
    CONSTRAINT interfaces FOREIGN KEY (interface_id)
        REFERENCES bsd_stat.interfaces (interface_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT parameters FOREIGN KEY (param_id)
        REFERENCES bsd_stat.parameters (param_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE bsd_stat.netstat_values
    OWNER to postgres;