import psycopg2
import os
from patient import getalltriagepatients


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
        cur.execute("SELECT * FROM public."'tbl_triagepatient'";")
        result = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        newResults = getalltriagepatients(result)

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

        sql = "DELETE FROM public.tbl_triagepatient where fhirpatientid = %s;"
        cur.execute(sql, (idFHIR,))
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


def addPatientDetail(triagePatientId, practionerId, firstEncounterDate, dischargeDate, active):
    """ Connect to the PostgreSQL database server """
    TriagePatientdetailId = 0
    conn = None
    try:
        conn = psycopg2.connect(get_connection_to_db())
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public."'tbl_triagepatientdetail'"(TriagePatientId,TriagePractionerId, FirstEncounterDate,
                                DischargeDate,Active)
                         VALUES(%s1,%s2,%s3,%s4,%s5) RETURNING TriagePatientDetailId;"""
        cur.execute(sql, (triagePatientId, practionerId, firstEncounterDate, dischargeDate, active,))
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
        sql = """INSERT INTO public."'tbl_triagepatientstatus'"(TriagePatientDetailId,PatientCurrentLocation, TriageESIStatusId)
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
        sql = """INSERT INTO public."'tbl_triageprofessional'"(FHIRPractionerId,TriageWorkStatusId, ProfessionalType)
                         VALUES(%s1,%s2,%s3) RETURNING TriageProffesionalId;"""
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
