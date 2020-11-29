CREATE TABLE "tbl_triagepatient"

(

    "triagepatientid" BIGSERIAL NOT NULL,

    "fhirpatientid" text,

    PRIMARY KEY ("triagepatientid")

);

CREATE TABLE "tbl_triageprofessional"

(

    "triageprofessionalid" BIGSERIAL NOT NULL,

    "fhirpractionerid" text,

    "triageworkstatus" integer,

    "professionalType" text COLLATE pg_catalog."default",

    CONSTRAINT "tbl_triageprofessional_pkey" PRIMARY KEY ("triageprofessionalid")

);

CREATE TABLE "tbl_triagepatientdetail"

(

    "triagepatientdetailid" BIGSERIAL NOT NULL,

    "triagepatientid" bigint,

    "triagepractionerid" bigint,
	
	"patientcurrentlocation" text,
	
	"esi" text,

    "firstencounterdate" date,
	
	"lastseen" timestamp,

    "dischargedate" date,

    "active" boolean,

    CONSTRAINT "tbl_triagepatientdetail_pkey" PRIMARY KEY ("triagepatientdetailid"),

    CONSTRAINT "tbltriagepatient_tbltriagepatientdetail" FOREIGN KEY ("triagepatientid")

        REFERENCES "tbl_triagepatient" ("triagepatientid") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE CASCADE,

    CONSTRAINT "tbl_triagepatientdetail_triagepractionerid_fkey" FOREIGN KEY ("triagepractionerid")

        REFERENCES "tbl_triageprofessional" ("triageprofessionalid") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE CASCADE

);

CREATE TABLE "tbl_triagepatientevent"

(

    "triagepatienteventid" BIGSERIAL NOT NULL,

    "triagepatientdetailid" bigint,
	
	"event_type" text,

    "notes" text,
	
    "author" text,
	
	"event_time" timestamp default now(), 
	
    PRIMARY KEY ("triagepatienteventid"),

    FOREIGN KEY ("triagepatientdetailid")

        REFERENCES "tbl_triagepatientdetail" ("triagepatientdetailid") MATCH SIMPLE

        ON UPDATE NO ACTION

        ON DELETE CASCADE

);