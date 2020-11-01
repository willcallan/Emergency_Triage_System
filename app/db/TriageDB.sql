CREATE TABLE triage_patient

(

    triage_patient_id bigint NOT NULL,

    fhir_patient_id bigint,

    PRIMARY KEY (triage_patient_id)

);



ALTER TABLE triage_patient

    OWNER to edts;





-- Table: triage_patient_detail



-- DROP TABLE triage_patient_detail;



CREATE TABLE triage_patient_detail

(

    triage_patient_detail_id bigint NOT NULL,

    triage_patient_id bigint,

    triage_practioner_id bigint,

    first_encounter_date date,

    discharge_date date,

    active boolean

)



    TABLESPACE pg_default;



ALTER TABLE triage_patient_detail

    OWNER to edts;

-- Index: professional_id



-- DROP INDEX professional_id;



CREATE INDEX professional_id

    ON triage_patient_detail USING btree

        (triage_practioner_id ASC NULLS LAST)

    TABLESPACE pg_default;

CREATE TABLE triage_patient_status

(

    triage_patient_status_id bigint NOT NULL,

    triage_patient_detail_id bigint,

    patient_current_location text,

    triage_esi_status_id bigint,

    PRIMARY KEY (triage_patient_status_id)

);



ALTER TABLE triage_patient_status

    OWNER to edts;



-- Table: triage_esi_status



-- DROP TABLE triage_esi_status;



CREATE TABLE triage_esi_status

(

    triage_esi_status_id bigint NOT NULL,

    esi integer,

    code text COLLATE pg_catalog.default,

    display text COLLATE pg_catalog.default,

    date_created date,

    CONSTRAINT triage_esi_status_pkey PRIMARY KEY (triage_esi_status_id)

)



    TABLESPACE pg_default;



ALTER TABLE triage_esi_status

    OWNER to edts;



-- Table: triage_professional



-- DROP TABLE triage_professional;



CREATE TABLE triage_professional

(

    triage_professional_id bigint NOT NULL,

    fhir_practioner_id bigint,

    triage_work_status_id bigint,

    professional_type text COLLATE pg_catalog.default,

    CONSTRAINT triage_professional_pkey PRIMARY KEY (triage_professional_id)

)



    TABLESPACE pg_default;



ALTER TABLE triage_professional

    OWNER to edts;



-- Table: TriageErrorLog



-- DROP TABLE TTbl_riageErrorLog;



CREATE TABLE triage_error_log

(

    triage_log_id bigint,

    error_description text COLLATE pg_catalog.default,

    time_stamp_created date

)



    TABLESPACE pg_default;



ALTER TABLE triage_error_log

    OWNER to edts;



-- Table: triage_work_status



-- DROP TABLE triage_work_status;



CREATE TABLE triage_work_status

(

    triage_work_status_id bigint NOT NULL,

    long_description text COLLATE pg_catalog.default,

    short_description text COLLATE pg_catalog.default,

    date_created date,

    CONSTRAINT triage_work_status_pkey PRIMARY KEY (triage_work_status_id)

)



    TABLESPACE pg_default;



ALTER TABLE triage_work_status

    OWNER to edts;
