CREATE TABLE "tbl_triagepatient"

(

    "triagepatientid" bigint NOT NULL,

    "fhirpatientid" text,

    PRIMARY KEY ("triagepatientid")

);

CREATE TABLE "tbl_triageprofessional"

(

    "triageprofessionalid" bigint NOT NULL,

    "fhirpractionerid" text,

    "triageworkstatusid" bigint,

    "professionalType" text COLLATE pg_catalog."default",

    CONSTRAINT "tbl_triageprofessional_pkey" PRIMARY KEY ("triageprofessionalid")

);

CREATE TABLE "tbl_triagepatientdetail"

(

    "triagepatientdetailid" bigint NOT NULL,

    "triagepatientid" bigint,

    "triagepractionerid" bigint,

    "firstencounterdate" date,

    "dischargedate" date,

    "active" boolean,

    CONSTRAINT "tbl_triagepatientdetail_pkey" PRIMARY KEY ("triagepatientdetailid"),

    CONSTRAINT "tbltriagepatient_tbltriagepatientdetail" FOREIGN KEY ("triagepatientid")

        REFERENCES "tbl_triagepatient" ("triagepatientid") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION,

    CONSTRAINT "tbl_triagepatientdetail_triagepractionerid_fkey" FOREIGN KEY ("triagepractionerid")

        REFERENCES "tbl_triageprofessional" ("triageprofessionalid") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



);

CREATE TABLE "tbl_triagepatientstatus"

(

    "triagepatientstatusid" bigint NOT NULL,

    "triagepatientdetailid" bigint,

    "patientcurrentlocation" text,

    "triageesistatusid" bigint,

    PRIMARY KEY ("triagepatientstatusid"),

    FOREIGN KEY ("triagepatientdetailid")

        REFERENCES "tbl_triagepatientdetail" ("triagepatientdetailid") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE NO ACTION



);

CREATE TABLE "tbl_triageesistatus"

(

    "triageesistatusid" bigint NOT NULL,

    "esi" integer,

    "code" text COLLATE pg_catalog."default",

    "display" text COLLATE pg_catalog."default",

    "datecreated" date,

    CONSTRAINT "tbl_triageesistatus_pkey" PRIMARY KEY ("triageesistatusid")

);

CREATE TABLE "tbl_triageerrorlog"

(

    "triagelogid" bigint,

    "errordescription" text COLLATE pg_catalog."default",

    "timestampcreated" date

);

CREATE TABLE "tbl_triageworkstatus"

(

    "triageworkstatusid" bigint NOT NULL,

    "longdescription" text COLLATE pg_catalog."default",

    "shortdescription" text COLLATE pg_catalog."default",

    "datecreated" date,

    CONSTRAINT "triageworkstatus_pkey" PRIMARY KEY ("triageworkstatusid")

);

INSERT INTO "tbl_triagepatient" ("fhirpatientid","triagepatientid") values ('fc200fa2-12c9-4276-ba4a-e0601d424e55',1);
INSERT INTO "tbl_triagepatient" ("fhirpatientid","triagepatientid") values ('689892bd-dcbe-41fc-8651-38a1d0893854',2);

INSERT INTO "tbl_triageprofessional" ("triageprofessionalid", "fhirpractionerid", "triageworkstatusid", "professionalType")
 VALUES (1, 'efb5d4ce-dffc-47df-aa6d-05d372fdb407',NULL,'Doctor');
INSERT INTO "tbl_triageprofessional" ("triageprofessionalid", "fhirpractionerid", "triageworkstatusid", "professionalType")
VALUES (1, '5e57a286-d7c6-4e2d-9834-7fb48bd32b51',NULL,'Doctor');

INSERT INTO "tbl_triagepatientdetail" ("triagepatientdetailid", "triagepatientid", "triagepractionerid", "firstencounterdate", "dischargedate", "active") VALUES
(1,1,1,'2020-10-28','2020-11-01',1);









