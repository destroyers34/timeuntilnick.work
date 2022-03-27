from imap_tools import MailBox, OR
import os
import mysql.connector

#ENV VARIABLES
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_NAME = os.environ['DB_NAME']
IMAPSERVER = os.environ['IMAP_SERVER']
USERNAME = os.environ['IMAP_USERNAME']
PASSWORD = os.environ['IMAP_PASSWORD']

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


def check_for_server(conn, server_to_check):
    mycursor = conn.cursor()
    query = "SELECT * FROM backuptracking WHERE server=%s"
    print("Query server: " + server_to_check + " in the DB")
    mycursor.execute(query, (server_to_check,))
    result = mycursor.fetchone()
    mycursor.close()
    return result


def update_stat_list(conn, server):
    mycursor = conn.cursor()
    if server['last_failed'] is None:
        last_failed = '1900-01-01'
    else:
        last_failed = server['last_failed'].strftime('%Y-%m-%d')
    if server['last_success'] is None:
        last_success = '1900-01-01'
    else:
        last_success = server['last_success'].strftime('%Y-%m-%d')
    failed_count = server['failed_count']
    last_error = server['last_error']
    hostname = server['server']

    query_insert_update = """
UPDATE `backuptracking` 
SET `last_failed`=if(`last_failed`<%s,%s,`last_failed`),`last_success`=if(`last_success`<%s,%s,`last_success`),`failed_count`=`failed_count`+%s,`last_error`=if(%s,%s,`last_error`) 
WHERE server=%s"""
    print("Running QUERY:")
    mycursor.execute(query_insert_update,
                     (last_failed, last_failed, last_success, last_success, failed_count, last_error, last_error,
                      hostname,))
    print(mycursor.statement)
    print("Updated server " + hostname + " in the DB")
    mycursor.close()
    return None


def insert_into_stat_list(conn, server):
    mycursor = conn.cursor()
    if server['last_failed'] is None:
        last_failed = '1900-01-01'
    else:
        last_failed = server['last_failed']

    if server['last_success'] is None:
        last_success = '1900-01-01'
    else:
        last_success = server['last_success']

    failed_count = server['failed_count']
    last_error = server['last_error']
    hostname = server['server']

    query_insert_new = """
INSERT INTO `backuptracking`(`server`, `last_failed`, `last_success`, `failed_count`, `last_error`) 
VALUES (%s,%s,%s,%s,%s)"""
    mycursor.execute(query_insert_new, (hostname, last_failed, last_success, failed_count, last_error,))
    print("Inserted server " + hostname + " in the DB")
    mycursor.close()
    return None


def check_backup_notification(mailbox, folder, subjects):
    print(mailbox.folder.status(folder))
    mailbox.folder.set(folder)
    query = OR(subject=subjects)
    messages = list(mailbox.fetch(criteria=query, charset='utf-8', mark_seen=False, bulk=False))
    return messages


def update_serverlist_failed(mailbox, serverlist):
    failed_folder = 'INBOX.Backup Alerts.Backup Failed'
    failed_subjects = ['The backup process failed', 'Le processus de sauvegarde a']
    for msg in check_backup_notification(mailbox, failed_folder, failed_subjects):
        last_error = msg.text.split("\r\n\r\n")[2]
        try:
            serverlist[msg.subject.split(".")[0][1:]].update(
                {'server': msg.subject.split("]")[0][1:],
                 'failed_count': serverlist[msg.subject.split(".")[0][1:]]['failed_count'] + 1,
                 'last_failed': msg.date,
                 'last_error': last_error})
        except KeyError:
            serverlist[msg.subject.split(".")[0][1:]] = {'server': msg.subject.split("]")[0][1:],
                                                         'failed_count': 1,
                                                         'last_failed': msg.date,
                                                         'last_error': last_error,
                                                         'last_success': None}
        mailbox.delete(msg.uid)
    return serverlist


def update_serverlist_success(mailbox, serverlist):
    success_folder = 'INBOX.Backup Alerts.Backup Success'
    success_subjects = ['The backup process completed', 'Le processus de sauvegarde est termin']
    for msg in check_backup_notification(mailbox, success_folder, success_subjects):
        try:
            serverlist[msg.subject.split(".")[0][1:]].update(
                {'server': msg.subject.split("]")[0][1:], 'last_success': msg.date})
        except KeyError:
            serverlist[msg.subject.split(".")[0][1:]] = {'server': msg.subject.split("]")[0][1:],
                                                         'failed_count': 0,
                                                         'last_failed': None,
                                                         'last_error': None,
                                                         'last_success': msg.date}
        mailbox.delete(msg.uid)
    return serverlist


def check_mail():
    serverlist = {}
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    with MailBox(IMAPSERVER).login(USERNAME, PASSWORD) as mailbox:
        serverlist = update_serverlist_failed(mailbox, serverlist)
        serverlist = update_serverlist_success(mailbox, serverlist)
    for server in serverlist.values():
        if check_for_server(conn, server['server']):
            update_stat_list(conn, server)
        else:
            insert_into_stat_list(conn, server)
    conn.close()


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