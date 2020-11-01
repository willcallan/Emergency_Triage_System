CREATE TABLE "Tbl_TriagePatient"

(

    "TriagePatientId" bigint NOT NULL,

    "FHIRPatientId" text,

    PRIMARY KEY ("TriagePatientId")

);

CREATE TABLE "Tbl_TriageProfessional"

(

    "TriageProfessionalId" bigint NOT NULL,

    "FHIRPractionerId" text,

    "TriageWorkStatusId" bigint,

    "ProfessionalType" text COLLATE pg_catalog."default",

    CONSTRAINT "Tbl_TriageProfessional_pkey" PRIMARY KEY ("TriageProfessionalId")

);

CREATE TABLE "Tbl_TriagePatientDetail"

(

    "TriagePatientDetailId" bigint NOT NULL,

    "TriagePatientId" bigint,

    "TriagePractionerId" bigint,

    "FirstEncounterDate" date,

    "DischargeDate" date,

    "Active" boolean,

    CONSTRAINT "Tbl_TriagePatientDetail_pkey" PRIMARY KEY ("TriagePatientDetailId"),

    CONSTRAINT "TblTriagePatient_TblTriagePatientDetail" FOREIGN KEY ("TriagePatientId")

        REFERENCES "Tbl_TriagePatient" ("TriagePatientId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION,

    CONSTRAINT "Tbl_TriagePatientDetail_TriagePractionerId_fkey" FOREIGN KEY ("TriagePractionerId")

        REFERENCES "Tbl_TriageProfessional" ("TriageProfessionalId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



);

CREATE TABLE "Tbl_TriagePatientStatus"

(

    "TriagePatientStatusId" bigint NOT NULL,

    "TriagePatientDetailId" bigint,

    "PatientCurrentLocation" text,

    "TriageESIStatusId" bigint,

    PRIMARY KEY ("TriagePatientStatusId"),

    FOREIGN KEY ("TriagePatientDetailId")

        REFERENCES "Tbl_TriagePatientDetail" ("TriagePatientDetailId") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



);

CREATE TABLE "Tbl_TriageESIStatus"

(

    "TriageESIStatusId" bigint NOT NULL,

    "ESI" integer,

    "Code" text COLLATE pg_catalog."default",

    "Display" text COLLATE pg_catalog."default",

    "DateCreated" date,

    CONSTRAINT "Tbl_TriageESIStatus_pkey" PRIMARY KEY ("TriageESIStatusId")

);

CREATE TABLE "Tbl_TriageErrorLog"

(

    "TriageLogId" bigint,

    "ErrorDescription" text COLLATE pg_catalog."default",

    "TimeStampCreated" date

);

CREATE TABLE "Tbl_TriageWorkStatus"

(

    "TriageWorkStatusId" bigint NOT NULL,

    "LongDescription" text COLLATE pg_catalog."default",

    "ShortDescription" text COLLATE pg_catalog."default",

    "DateCreated" date,

    CONSTRAINT "TriageWorkStatus_pkey" PRIMARY KEY ("TriageWorkStatusId")

);

INSERT INTO "Tbl_TriagePatient" ("FHIRPatientId","TriagePatientId") values ('fc200fa2-12c9-4276-ba4a-e0601d424e55',1);
INSERT INTO "Tbl_TriagePatient" ("FHIRPatientId","TriagePatientId") values ('689892bd-dcbe-41fc-8651-38a1d0893854',2);

INSERT INTO "Tbl_TriageProfessional" ("TriageProfessionalId", "FHIRPractionerId", "TriageWorkStatusId", "ProfessionalType")
 VALUES (1, 'efb5d4ce-dffc-47df-aa6d-05d372fdb407',NULL,'Doctor');
INSERT INTO "Tbl_TriageProfessional" ("TriageProfessionalId", "FHIRPractionerId", "TriageWorkStatusId", "ProfessionalType")
VALUES (1, '5e57a286-d7c6-4e2d-9834-7fb48bd32b51',NULL,'Doctor');

INSERT INTO "Tbl_TriagePatientDetail" ("TriagePatientDetailId", "TriagePatientId", "TriagePractionerId", "FirstEncounterDate", "DischargeDate", "Active") VALUES
(1,1,1,'2020-10-28','2020-11-01',1);









