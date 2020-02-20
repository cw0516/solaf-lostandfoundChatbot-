import pymysql
import pandas as pd


host_name = "localhost"
username = ""
password = ""
database_name = "lostandfound"


def make_date_query(search_dates):
    SQL_date = "SELECT * FROM lostinfo WHERE (date = "
    for i, date in enumerate(search_dates):
        if i == 0:
            SQL_date += "\'{}\'".format(date)
        else:
            SQL_date += " OR date = \'{}\' ".format(date)
    SQL_date += ')'
    return SQL_date

def make_connection():

    db_lost = pymysql.connect(
        host=host_name,  # DATABASE_HOST
        port=3306,
        user=username,  # DATABASE_USERNAME
        passwd=password,  # DATABASE_PASSWORD
        db=database_name,  # DATABASE_NAME
        charset='utf8'
    )
    return db_lost


def select_by_dates(search_dates):
    conn = make_connection()
    sql = make_date_query(search_dates)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def select_by_dates_and_description(search_dates,tag,color):

    sql = make_date_query(search_dates)
    if color:
        sql += "and tag = '{}'".format(tag)
        sql += "and description = '{}'".format(color)
    else:
        sql += "and tag = '{}'".format(tag)

    conn = make_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def select_by_id(id):
    conn = make_connection()
    sql = "SELECT * FROM lostinfo WHERE id = '{}'".format(id)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df