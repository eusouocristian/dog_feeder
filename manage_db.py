import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def insert_prog(conn, programas):
    with conn:
        sql = ''' INSERT INTO PROGRAMAS(TimeStamp,P1,P2,P3)
                VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, programas)
        conn.commit()
        # Return ID
        return cur.lastrowid

def get_last_prog(conn):
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM PROGRAMAS \
                    ORDER BY TimeStamp DESC \
                    LIMIT 1;")
        output = cur.fetchall()
        return output
