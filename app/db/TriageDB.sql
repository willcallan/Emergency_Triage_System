-- Database: TriageDB



-- DROP DATABASE "TriageDB";



CREATE DATABASE "TriageDB"

    WITH

    OWNER = postgres

    ENCODING = 'UTF8'

    LC_COLLATE = 'English_United States.1252'

    LC_CTYPE = 'English_United States.1252'

    TABLESPACE = pg_default

    CONNECTION LIMIT = -1;





CREATE TABLE public."Tbl_TriagePatient"

(

    "TriagePatientId" bigint NOT NULL,

    "FHIRPatientId" bigint,

    PRIMARY KEY ("TriagePatientId")

);



ALTER TABLE public."Tbl_TriagePatient"

    OWNER to postgres;





-- Table: public.Tbl_TriagePatientDetail



-- DROP TABLE public."Tbl_TriagePatientDetail";



CREATE TABLE public."Tbl_TriagePatientDetail"

(

    "TriagePatientDetailId" bigint NOT NULL,

    "TriagePatientId" bigint,

    "TriagePractionerId" bigint,

    "FirstEncounterDate" date,

    "DischargeDate" date,

    "Active" boolean,

    CONSTRAINT "Tbl_TriagePatientDetail_pkey" PRIMARY KEY ("TriagePatientDetailId"),

    CONSTRAINT "TblTriagePatient_TblTriagePatientDetail" FOREIGN KEY ("TriagePatientId")

        REFERENCES public."Tbl_TriagePatient" ("TriagePatientId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION,

    CONSTRAINT "Tbl_TriagePatientDetail_TriagePractionerId_fkey" FOREIGN KEY ("TriagePractionerId")

        REFERENCES public."Tbl_TriageProfessional" ("TriageProfessionalId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



)



    TABLESPACE pg_default;



ALTER TABLE public."Tbl_TriagePatientDetail"

    OWNER to postgres;

-- Index: ProfessionalId



-- DROP INDEX public."ProfessionalId";



CREATE INDEX "ProfessionalId"

    ON public."Tbl_TriagePatientDetail" USING btree

        ("TriagePractionerId" ASC NULLS LAST)

    TABLESPACE pg_default;

CREATE TABLE public."Tbl_TriagePatientStatus"

(

    "TriagePatientStatusId" bigint NOT NULL,

    "TriagePatientDetailId" bigint,

    "PatientCurrentLocation" text,

    "TriageESIStatusId" bigint,

    PRIMARY KEY ("TriagePatientStatusId"),

    FOREIGN KEY ("TriagePatientDetailId")

        REFERENCES public."Tbl_TriagePatientDetail" ("TriagePatientDetailId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



);



ALTER TABLE public."Tbl_TriagePatientStatus"

    OWNER to postgres;



-- Table: public.Tbl_TriageESIStatus



-- DROP TABLE public."Tbl_TriageESIStatus";



CREATE TABLE public."Tbl_TriageESIStatus"

(

    "TriageESIStatusId" bigint NOT NULL,

    "ESI" integer,

    "Code" text COLLATE pg_catalog."default",

    "Display" text COLLATE pg_catalog."default",

    "DateCreated" date,

    CONSTRAINT "Tbl_TriageESIStatus_pkey" PRIMARY KEY ("TriageESIStatusId")

)



    TABLESPACE pg_default;



ALTER TABLE public."Tbl_TriageESIStatus"

    OWNER to postgres;



-- Table: public.Tbl_TriageProfessional



-- DROP TABLE public."Tbl_TriageProfessional";



CREATE TABLE public."Tbl_TriageProfessional"

(

    "TriageProfessionalId" bigint NOT NULL,

    "FHIRPractionerId" bigint,

    "TriageWorkStatusId" bigint,

    "ProfessionalType" text COLLATE pg_catalog."default",

    CONSTRAINT "Tbl_TriageProfessional_pkey" PRIMARY KEY ("TriageProfessionalId")

)



    TABLESPACE pg_default;



ALTER TABLE public."Tbl_TriageProfessional"

    OWNER to postgres;



-- Table: public.TriageErrorLog



-- DROP TABLE public."TTbl_riageErrorLog";



CREATE TABLE public."Tbl_TriageErrorLog"

(

    "TriageLogId" bigint,

    "ErrorDescription" text COLLATE pg_catalog."default",

    "TimeStampCreated" date

)



    TABLESPACE pg_default;



ALTER TABLE public."Tbl_TriageErrorLog"

    OWNER to postgres;



-- Table: public.Tbl_TriageWorkStatus



-- DROP TABLE public."Tbl_TriageWorkStatus";



CREATE TABLE public."Tbl_TriageWorkStatus"

(

    "TriageWorkStatusId" bigint NOT NULL,

    "LongDescription" text COLLATE pg_catalog."default",

    "ShortDescription" text COLLATE pg_catalog."default",

    "DateCreated" date,

    CONSTRAINT "TriageWorkStatus_pkey" PRIMARY KEY ("TriageWorkStatusId")

)



    TABLESPACE pg_default;



ALTER TABLE public."Tbl_TriageWorkStatus"

    OWNER to postgres;