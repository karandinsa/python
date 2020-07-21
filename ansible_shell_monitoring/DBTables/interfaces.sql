-- Table: bsd_stat.interfaces

-- DROP TABLE bsd_stat.interfaces;

CREATE TABLE bsd_stat.interfaces
(
    interface_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(200) COLLATE pg_catalog."default" NOT NULL DEFAULT 'n/a'::character varying,
    network character varying(200) COLLATE pg_catalog."default" NOT NULL DEFAULT 'n/a'::character varying,
    address character varying(200) COLLATE pg_catalog."default" NOT NULL DEFAULT 'n/a'::character varying,
    host_id bigint NOT NULL DEFAULT 5,
    CONSTRAINT interfaces_pkey PRIMARY KEY (interface_id),
    CONSTRAINT interface UNIQUE (name, network, address, host_id),
    CONSTRAINT ansible_hosts FOREIGN KEY (host_id)
        REFERENCES bsd_stat.ansible_hosts (host_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE bsd_stat.interfaces
    OWNER to postgres;