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
        cur.execute("SELECT * FROM public.tbl_triagepatient where active = true;")
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


def addPatient(idFHIR):
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


def addPatientDetail(triagePatientId, practionerId, currentLocation, esi,
                     firstEncounterDate, lastseen, dischargeDate, active):
    """ Connect to the PostgreSQL database server """
    TriagePatientdetailId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triagepatientdetail (triagepatientid, triagepractionerid, 
                        patientcurrentlocation, esi, firstencounterdate, lastseen, dischargedate, active)
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING triagepatientdetailid;"""
        cur.execute(sql, (triagePatientId, practionerId, currentLocation, esi, firstEncounterDate,
                          lastseen, dischargeDate, active,))
        TriagePatientdetailId = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return TriagePatientdetailId


def addPatientEvent(triagepatientdetailid, event_type, notes, author):
    """ Connect to the PostgreSQL database server """
    triagepatienteventid = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triagepatientevent (triagepatientdetailid, event_type, 
                        notes, author)
                         VALUES(%s,%s,%s,%s) RETURNING triagepatienteventid;"""
        cur.execute(sql, (triagepatientdetailid,event_type,notes,author))
        triagepatienteventid = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return triagepatienteventid


def addPractioner(practionaerFHIRId, triageworkstatus, professionalType):
    """ Connect to the PostgreSQL database server """
    TriagePractionerId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public.tbl_triageprofessional (fhirpractionerid, triageworkstatus,"professionalType")
                         VALUES(%s,%s,%s) RETURNING triageprofessionalid;"""
        cur.execute(sql, (practionaerFHIRId, triageworkstatus, professionalType,))
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
            sql = "SELECT triagepatientid FROM public.tbl_triagepatient where fhirpatientid = %s;"

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


def getPatientEventsFromFhirId(idFHIR):
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

        sql = "SELECT triagepatienteventid, event_type, notes, author, to_char(event_time, 'YYYY-MM-DDThh:mm:ss') " \
              "FROM public.tbl_triagepatientevent e " \
              "join tbl_triagepatientdetail d on e.triagepatientdetailid = d.triagepatientdetailid " \
              "join tbl_triagepatient p on p.triagepatientid = d.triagepatientid where p.fhirpatientid = %s;"
        cur.execute(sql,(idFHIR,))
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return result


def getPatientDetailsFromFhir(idFHIR):
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

        sql = "SELECT patientcurrentlocation, esi, firstencounterdate, to_char(lastseen, 'YYYY-MM-DDThh:mm:ss'), " \
              "dischargedate, r.fhirpractionerid " \
              "FROM public.tbl_triagepatient p " \
              "join tbl_triagepatientdetail d on p.triagepatientid = d.triagepatientid " \
              "left join tbl_triageProfessional r on d.triagepractionerid = r.triageprofessionalid " \
              "where p.fhirpatientid = %s;"
        cur.execute(sql,(idFHIR,))
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return result

def getPatientDetailIdFromFhir(idFHIR):
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

        sql = "SELECT d.triagepatientdetailid " \
              "FROM public.tbl_triagepatient p " \
              "join tbl_triagepatientdetail d on p.triagepatientid = d.triagepatientid " \
              "where p.fhirpatientid = %s;"
        cur.execute(sql,(idFHIR,))
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return result


def updatePatientDetail(triagepatientid, triagepractionerid, patientcurrentlocation, esi, lastseen):

    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """UPDATE public.tbl_triagepatientdetail set triagepractionerid = %s, patientcurrentlocation = %s,
                        esi = %s, lastSeen = %s where triagepatientid = %s"""
        cur.execute(sql, (triagepractionerid, patientcurrentlocation, esi, lastseen, triagepatientid,))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            conn.close()
        return True


def patientExistsInDB(idFHIR):
    """ Connect to the PostgreSQL database server """
    TriagePatientId = ''
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """select triagepatientid from tbl_triagepatient where fhirpatientid = %s"""
        cur.execute(sql, (idFHIR,))
        TriagePatientId = cur.fetchone()[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return TriagePatientId != ''


def updateLastSeen(idFHIR):
    """ Connect to the PostgreSQL database server """
    TriagePatientId = ''
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """update tbl_triagepatientdetail as d set lastseen = now() 
        from tbl_triagepatient p where p.triagepatientid = d.triagepatientid and p.fhirpatientid = %s"""
        cur.execute(sql, (idFHIR,))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return False
    finally:
        if conn is not None:
            conn.close()
        return True


def getPractWorkStatusByFhir(practionaerFHIRId):
    """ Connect to the PostgreSQL database server """
    PractitionerWorkStatus = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """select triageworkstatus from tbl_triageprofessional where fhirpractionerid = %s"""
        cur.execute(sql, (practionaerFHIRId,))
        PractitionerWorkStatus = cur.fetchone()[0]
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return PractitionerWorkStatus


def dischargePatient(idFHIR):
    """ Connect to the PostgreSQL database server """
    TriagePatientId = ''
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """update tbl_triagepatientdetail as d set dischargedate = now(), active = false 
        from tbl_triagepatient p where p.triagepatientid = d.triagepatientid and p.fhirpatientid = %s"""
        cur.execute(sql, (idFHIR,))
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return False
    finally:
        if conn is not None:
            conn.close()
        return True
