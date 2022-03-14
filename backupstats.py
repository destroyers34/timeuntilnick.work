import os
import mysql.connector

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
mycursor = conn.cursor()


def get_server_list():
    q_get_stat_list = "SELECT * FROM backuptracking ORDER BY last_failed DESC, failed_count DESC;"
    mycursor.execute(q_get_stat_list)
    return mycursor.fetchall()


def get_failed_server_list():
    q_get_stat_list = "SELECT * FROM backuptracking WHERE last_success < last_failed ORDER BY last_failed DESC, failed_count DESC;"
    mycursor.execute(q_get_stat_list)
    return mycursor.fetchall()


def get_success_server_list():
    q_get_stat_list = "SELECT * FROM backuptracking WHERE last_success > last_failed ORDER BY last_success DESC;"
    mycursor.execute(q_get_stat_list)
    return mycursor.fetchall()


if __name__ == '__main__':
    print(get_server_list())