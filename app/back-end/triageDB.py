import psycopg2
import os
from patient import get_all_triage_patients
from practitioner import get_all_triage_practitioners


def get_connection_to_db():
    return "host={host} port={port} dbname={dbname} user={user} password={password}".format(
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'))


def getallPatient():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute("SELECT * FROM public.tbl_triagepatient;")
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        newResults = get_all_triage_patients(result)

        return newResults


def getallPatientIds():
    """ Connect to the PostgreSQL database server """
    conn = None
    result = []
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        cur = conn.cursor()

        cur.execute("SELECT fhirpatientid FROM public.tbl_triagepatient;")
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def getAllPractitionerIds():
    """ Connect to the PostgreSQL database server """
    conn = None
    result = []
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        cur = conn.cursor()

        cur.execute("SELECT fhirpractionerid FROM public.tbl_triageprofessional;")
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def deletePatientByFhirId(idFHIR):
    """ Connect to the PostgreSQL database server """
    conn = None
    result = []
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        cur = conn.cursor()

        sql = "DELETE FROM public.tbl_triagepatient where fhirpatientid = %s"
        cur.execute(sql,(idFHIR,))
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def deletePractitionerbyFhirId(idFHIR):
    """ Connect to the PostgreSQL database server """
    conn = None
    result = []
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        cur = conn.cursor()

        sql = "DELETE FROM public.tbl_triageprofessional where fhirpractionerid = %s"
        cur.execute(sql,(idFHIR,))
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def getPatientDetailById(FHIRId):
    conn = None

    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute(
            "SELECT patientcurrentlocation, triageesistatusid FROM public."'tbl_triagepatientdetail'" as td inner join public."'tbl_triagepatient'" as tp"+
        +" on td.TriagePatientId = tp.TriagePatientId "+
        +" inner join public."'tbl_triagepatientstatus'" as tps "+
        +" on tps.triagepatientdetailid = td.triagepatientdetailid "+
        +" inner join public."'tbl_triageprofessional'" as tpp "+
        +" on tpp.triageprofessionalid = td.triagepractionerid "+
        +" where FHIRPatientId="+"'" + "%s" + "'", (FHIRId,))
        result = cur.fetchall()


        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return result




def addPatients(idFHIR):
    """ Connect to the PostgreSQL database server """
    TriagePatientId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triagepatient (FHIRPatientId)
                     VALUES(%s) RETURNING TriagePatientId;"""
        cur.execute(sql, (idFHIR,))
        TriagePatientId = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return TriagePatientId


def addPatientDetail(triagePatientId, practionerId, firstEncounterDate, lastseendate, dischargeDate, active):
    """ Connect to the PostgreSQL database server """
    TriagePatientdetailId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triagepatientdetail (triagepatientid, triagepractionerid, firstencounterdate, 
                        lastseendate, dischargedate, active)
                         VALUES(%s,%s,%s,%s,%s,%s) RETURNING triagepatientdetailid;"""
        cur.execute(sql, (triagePatientId, practionerId, firstEncounterDate, lastseendate, dischargeDate, active,))
        TriagePatientdetailId = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return TriagePatientdetailId


def addPatientStatus(PatientdetailId, patientcurrentlocation, esistatusId):
    """ Connect to the PostgreSQL database server """
    TriagePatientstatusId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triagepatientstatus (TriagePatientDetailId,PatientCurrentLocation, TriageESIStatusId)
                         VALUES(%s1,%s2,%s3) RETURNING TriagePatientStatusId;"""
        cur.execute(sql, (PatientdetailId, patientcurrentlocation, esistatusId,))
        TriagePatientstatusId = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return TriagePatientstatusId


def addPractioner(practionaerFHIRId, workStatusId, professionalType):
    """ Connect to the PostgreSQL database server """
    TriagePractionerId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triageprofessional (fhirpractionerid,triageworkstatusid,"professionalType")
                         VALUES(%s,%s,%s) RETURNING triageprofessionalid;"""
        cur.execute(sql, (practionaerFHIRId, workStatusId, professionalType,))
        TriagePractionerId = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return TriagePractionerId


def getAllPractitioner():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute("SELECT * FROM public.tbl_triageprofessional;")
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        newResults = get_all_triage_practitioners(result)

        return newResults


def translateFhirIdtoLocalId(fhir_id, fhir_object):
    """ Connect to the PostgreSQL database server """
    conn = None
    import fhirclient.models.practitioner as pract
    import fhirclient.models.patient as pat
    result = ""
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(get_connection_to_db())

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')

        if isinstance(fhir_object, pract.Practitioner):
            sql = "SELECT triageprofessionalid FROM public.tbl_triageprofessional where fhirpractionerid = %s;"

        if isinstance(fhir_object, pat.Patient):
            sql = "SELECT triagepatientid FROM public.tbl_triageprofessional where fhirpatientid = %s;"

        cur.execute(sql, (fhir_id,))
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return result

