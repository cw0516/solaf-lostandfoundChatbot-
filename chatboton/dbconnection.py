# -*- coding: utf-8 -*-

import pymysql

# database에 접근
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='',
                     passwd='',
                     db='test',
                     charset='utf8')

cursor = db.cursor()

sql = '''CREATE TABLE LEEJUNKI(
         idx  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(256) NOT NULL,
         nick VARCHAR(256) NOT NULL
         );'''

# SQL query 실행
cursor.execute(sql)

