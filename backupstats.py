import os
import mysql.connector

#ENV VARIABLES
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_NAME = os.environ['DB_NAME']

conn = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
conn.autocommit = True



def get_server_list(conn):
    mycursor = conn.cursor()
    q_get_stat_list = "SELECT * FROM backuptracking ORDER BY last_failed DESC, failed_count DESC;"
    mycursor.execute(q_get_stat_list)
    results = mycursor.fetchall()
    mycursor.close()
    return results


def get_failed_server_list(conn):
    mycursor = conn.cursor()
    q_get_stat_list = "SELECT * FROM backuptracking WHERE last_success < last_failed ORDER BY last_failed DESC, failed_count DESC;"
    mycursor.execute(q_get_stat_list)
    results = mycursor.fetchall()
    mycursor.close()
    return results


def get_success_server_list(conn):
    mycursor = conn.cursor()
    q_get_stat_list = "SELECT * FROM backuptracking WHERE last_success > last_failed ORDER BY last_success DESC;"
    mycursor.execute(q_get_stat_list)
    results = mycursor.fetchall()
    mycursor.close()
    return results


if __name__ == '__main__':
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    conn.autocommit = True
    print(get_server_list(conn))
    conn.close()