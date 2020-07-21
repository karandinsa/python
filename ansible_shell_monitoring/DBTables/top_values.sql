-- Table: bsd_stat.top_values

-- DROP TABLE bsd_stat.top_values;

CREATE TABLE bsd_stat.top_values
(
    top_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    param_id bigint NOT NULL DEFAULT 32,
    param_value numeric(26,6),
    epochtime bigint,
    ansible_host_id bigint NOT NULL DEFAULT 5,
    CONSTRAINT top_values_pkey PRIMARY KEY (top_id),
    CONSTRAINT uniq_value UNIQUE (param_id, epochtime, ansible_host_id),
    CONSTRAINT ansible_hosts FOREIGN KEY (ansible_host_id)
        REFERENCES bsd_stat.ansible_hosts (host_id) MATCH SIMPLE
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

ALTER TABLE bsd_stat.top_values
    OWNER to postgres;