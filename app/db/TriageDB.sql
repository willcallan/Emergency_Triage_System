<<<<<<< HEAD
CREATE TABLE triage_patient
=======
CREATE TABLE "tbl_triagepatient"
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

(

    triage_patient_id bigint NOT NULL,

<<<<<<< HEAD
    fhir_patient_id bigint,
=======
    "FHIRPatientId" text,
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

    PRIMARY KEY (triage_patient_id)

);

CREATE TABLE "tbl_triageprofessional"

(

<<<<<<< HEAD
ALTER TABLE triage_patient

    OWNER to edts;





-- Table: triage_patient_detail
=======
    "TriageProfessionalId" bigint NOT NULL,
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

    "FHIRPractionerId" text,

    "TriageWorkStatusId" bigint,

<<<<<<< HEAD
-- DROP TABLE triage_patient_detail;
=======
    "ProfessionalType" text COLLATE pg_catalog."default",
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

    CONSTRAINT "tbl_triageprofessional_pkey" PRIMARY KEY ("TriageProfessionalId")

);

<<<<<<< HEAD
CREATE TABLE triage_patient_detail
=======
CREATE TABLE "tbl_triagepatientdetail"
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

(

    triage_patient_detail_id bigint NOT NULL,

    triage_patient_id bigint,

    triage_practioner_id bigint,

<<<<<<< HEAD
    first_encounter_date date,
=======
    "FirstEncounterDate" date,

    "DischargeDate" date,

    "Active" boolean,

    CONSTRAINT "tbl_triagepatientdetail_pkey" PRIMARY KEY ("TriagePatientDetailId"),

    CONSTRAINT "tblTriagePatient_tblTriagePatientDetail" FOREIGN KEY ("TriagePatientId")

        REFERENCES "tbl_triagepatient" ("TriagePatientId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION,

    CONSTRAINT "tbl_triagepatientdetail_TriagePractionerId_fkey" FOREIGN KEY ("TriagePractionerId")

        REFERENCES "tbl_triageprofessional" ("TriageProfessionalId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

    discharge_date date,

    active boolean

<<<<<<< HEAD
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
=======
);

CREATE TABLE "tbl_triagepatientstatus"

(

    "TriagePatientStatusId" bigint NOT NULL,

    "TriagePatientDetailId" bigint,

    "PatientCurrentLocation" text,

    "TriageESIStatusId" bigint,

    PRIMARY KEY ("TriagePatientStatusId"),

    FOREIGN KEY ("TriagePatientDetailId")

        REFERENCES "tbl_triagepatientdetail" ("TriagePatientDetailId") MATCH SIMPLE
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

    triage_patient_detail_id bigint,

    patient_current_location text,

    triage_esi_status_id bigint,

    PRIMARY KEY (triage_patient_status_id)

);

<<<<<<< HEAD


ALTER TABLE triage_patient_status

    OWNER to edts;



-- Table: triage_esi_status



-- DROP TABLE triage_esi_status;



CREATE TABLE triage_esi_status
=======
CREATE TABLE "tbl_triageesistatus"
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

(

    triage_esi_status_id bigint NOT NULL,

    esi integer,

    code text COLLATE pg_catalog.default,

    display text COLLATE pg_catalog.default,

    date_created date,

<<<<<<< HEAD
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

=======
    CONSTRAINT "tbl_triageesistatus_pkey" PRIMARY KEY ("TriageESIStatusId")
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

);

<<<<<<< HEAD
CREATE TABLE triage_error_log
=======
CREATE TABLE "tbl_triageerrorlog"
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

(

    triage_log_id bigint,

    error_description text COLLATE pg_catalog.default,

    time_stamp_created date

<<<<<<< HEAD
)



    TABLESPACE pg_default;



ALTER TABLE triage_error_log

    OWNER to edts;



-- Table: triage_work_status



-- DROP TABLE triage_work_status;



CREATE TABLE triage_work_status
=======
);

CREATE TABLE "tbl_triageworkstatus"
>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772

(

    triage_work_status_id bigint NOT NULL,

    long_description text COLLATE pg_catalog.default,

    short_description text COLLATE pg_catalog.default,

    date_created date,

    CONSTRAINT triage_work_status_pkey PRIMARY KEY (triage_work_status_id)

);

INSERT INTO "tbl_triagepatient" ("FHIRPatientId","TriagePatientId") values ('fc200fa2-12c9-4276-ba4a-e0601d424e55',1);
INSERT INTO "tbl_triagepatient" ("FHIRPatientId","TriagePatientId") values ('689892bd-dcbe-41fc-8651-38a1d0893854',2);

INSERT INTO "tbl_triageprofessional" ("TriageProfessionalId", "FHIRPractionerId", "TriageWorkStatusId", "ProfessionalType")
 VALUES (1, 'efb5d4ce-dffc-47df-aa6d-05d372fdb407',NULL,'Doctor');
INSERT INTO "tbl_triageprofessional" ("TriageProfessionalId", "FHIRPractionerId", "TriageWorkStatusId", "ProfessionalType")
VALUES (1, '5e57a286-d7c6-4e2d-9834-7fb48bd32b51',NULL,'Doctor');

INSERT INTO "tbl_triagepatientdetail" ("TriagePatientDetailId", "TriagePatientId", "TriagePractionerId", "FirstEncounterDate", "DischargeDate", "Active") VALUES
(1,1,1,'2020-10-28','2020-11-01',1);








<<<<<<< HEAD
ALTER TABLE triage_work_status

    OWNER to edts;
=======

>>>>>>> 215aff01f2c28157d5ab208c380f6c6f9a15d772
