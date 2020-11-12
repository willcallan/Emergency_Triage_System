CREATE TABLE "tbl_triagepatient"

(

    "TriagePatientId" bigint NOT NULL,

    "FHIRPatientId" text,

    PRIMARY KEY ("TriagePatientId")

);

CREATE TABLE "tbl_triageprofessional"

(

    "TriageProfessionalId" bigint NOT NULL,

    "FHIRPractionerId" text,

    "TriageWorkStatusId" bigint,

    "ProfessionalType" text COLLATE pg_catalog."default",

    CONSTRAINT "tbl_triageprofessional_pkey" PRIMARY KEY ("TriageProfessionalId")

);

CREATE TABLE "tbl_triagepatientdetail"

(

    "TriagePatientDetailId" bigint NOT NULL,

    "TriagePatientId" bigint,

    "TriagePractionerId" bigint,

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

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



);

CREATE TABLE "tbl_triageesistatus"

(

    "TriageESIStatusId" bigint NOT NULL,

    "ESI" integer,

    "Code" text COLLATE pg_catalog."default",

    "Display" text COLLATE pg_catalog."default",

    "DateCreated" date,

    CONSTRAINT "tbl_triageesistatus_pkey" PRIMARY KEY ("TriageESIStatusId")

);

CREATE TABLE "tbl_triageerrorlog"

(

    "TriageLogId" bigint,

    "ErrorDescription" text COLLATE pg_catalog."default",

    "TimeStampCreated" date

);

CREATE TABLE "tbl_triageworkstatus"

(

    "TriageWorkStatusId" bigint NOT NULL,

    "LongDescription" text COLLATE pg_catalog."default",

    "ShortDescription" text COLLATE pg_catalog."default",

    "DateCreated" date,

    CONSTRAINT "TriageWorkStatus_pkey" PRIMARY KEY ("TriageWorkStatusId")

);

INSERT INTO "tbl_triagepatient" ("FHIRPatientId","TriagePatientId") values ('fc200fa2-12c9-4276-ba4a-e0601d424e55',1);
INSERT INTO "tbl_triagepatient" ("FHIRPatientId","TriagePatientId") values ('689892bd-dcbe-41fc-8651-38a1d0893854',2);

INSERT INTO "tbl_triageprofessional" ("TriageProfessionalId", "FHIRPractionerId", "TriageWorkStatusId", "ProfessionalType")
 VALUES (1, 'efb5d4ce-dffc-47df-aa6d-05d372fdb407',NULL,'Doctor');
INSERT INTO "tbl_triageprofessional" ("TriageProfessionalId", "FHIRPractionerId", "TriageWorkStatusId", "ProfessionalType")
VALUES (1, '5e57a286-d7c6-4e2d-9834-7fb48bd32b51',NULL,'Doctor');

INSERT INTO "tbl_triagepatientdetail" ("TriagePatientDetailId", "TriagePatientId", "TriagePractionerId", "FirstEncounterDate", "DischargeDate", "Active") VALUES
(1,1,1,'2020-10-28','2020-11-01',1);









