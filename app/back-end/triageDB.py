import psycopg2





def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        #params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            port="32778",
            database="edts",
            user="edts",
            password="newhat")

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

        return result


if __name__ == '__main__':
    connect()