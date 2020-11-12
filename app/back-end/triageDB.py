import psycopg2
from patient import getalltriagepatients

connectionToDB = {
    'host': 'localhost',
    'port': '32778',
    'database': 'edts',
    'user': 'edts',
    'password': 'newhat'
}


def getallPatient():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(connectionToDB)

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


def addPatients(idFHIR):
    """ Connect to the PostgreSQL database server """
    TriagePatientId = 0
    conn = None
    try:
        conn = psycopg2.connect(connectionToDB)
        # create a cursor
        cur = conn.cursor()
        sql = """INSERT INTO public."'tbl_triagepatient'"(FHIRPatientId)
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
        conn = psycopg2.connect(connectionToDB)
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
        conn = psycopg2.connect(connectionToDB)
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
        conn = psycopg2.connect(connectionToDB)
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

