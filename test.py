import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect('/Users/amoghvenkatesh/PycharmProjects/HackIllinois2019/venv/hackillinois.db')
        print(sqlite3.version)

        print("connected")
        cur = conn.cursor()
        rows = cur.execute('select * from EMPLOYEE_DATA')

        for x in rows:
            print(x)

        conn.commit()
        conn.close()
        #return conn
    except Error as e:
        print(e)

    return None


create_connection()