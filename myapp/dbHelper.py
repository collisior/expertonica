import sqlite3
from sqlite3 import Error
import pandas as pd
from .models import WebResult
import requests, time, datetime
from datetime import timedelta
import socket
from urllib.parse import urlparse

def create_connection(db_file):
    """ 
    Create a database connection to the SQLite database
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def migrate_excel_to_sqlite(conn, excel_file):
    """ 
    Migrate Excel sheet into the SQLite database
    :param conn: Connection object
    :param excel_file: database file
    """
    #upload excel into slqlite
    wb = pd.read_excel(excel_file)
    for sheet in wb:
        wb[sheet].to_sql(sheet, conn, index=False)
    conn.commit()

def drop_table_if_exists(conn, table_name):
    """
    Drop table
    :param conn: the Connection object
    :param table_name: string object table name
    """
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS " + table_name)
    conn.commit()
    print("table dropped successfully")


def get_all_rows(conn, table_name):
    """
    Query all rows in the rows table
    :param conn: the Connection object
    :param table_name: string object table name
    :return: list of all rows in the table
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table_name)

    rows = cur.fetchall()
    data = list()

    for row in rows:
        data.append(row)
    return data

def select_all_rows(conn, table_name):
    """
    Return all rows in the tasks table
    :param conn: the Connection object
    :param table_name: string object table name
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table_name)

    rows = cur.fetchall()
    return rows

def process_url(conn, url):
    """
    Process url and create WebResult object
    :param conn: the Connection object
    :param table_name: string object table name
    :return:
    """
    try:      
        urlinfo = urlparse(url[0])
        startTime = time.time()
        r = requests.get("http://" + url[0])
        timeout = time.time() - startTime
        dt = datetime.datetime.now()
        http_code = r.status_code
        ip = ""
        try:
            ip = socket.gethostbyname(urlinfo.netloc)
        except Exception as e:
            print('Error resolving DNS ' + e)

        wr = WebResult.objects.create(
            url=url[0],
            http_code=http_code,
            datetime=dt,
            ip=ip,
            timeout=float(timeout))
    except requests.exceptions.ConnectionError:
        print(url[0] + ": connection error")
        wr = WebResult.objects.create(
            url=url[0],
            http_code="connection error",
            datetime=datetime.datetime.now(),
            timeout=float(0))

"""
Parts of code was sourced from sqlitetutorial.net 
""" 