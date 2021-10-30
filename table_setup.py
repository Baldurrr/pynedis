#!/usr/bin/python3

import http.client
import json
from mysql.connector import errors
from environs import Env
import os
import time
from datetime import datetime,timedelta
import itertools

conn = mysql.connector.connect(user='xxxx',password='xxxx',host='xxxx',database='db_enedis',port=3307,auth_plugin='mysql_native_password')
cur = conn.cursor()
try:
    cur.execute("CREATE TABLE enedis_metrics (data_id INT NOT NULL AUTO_INCREMENT, time DATETIME, metric VARCHAR(20), conso_watt numeric(10,2), PRIMARY KEY(data_id))")
    print("Table created successfully")
except mysql.connector.Error as e:
    print(e)

try: 
    cur.execute("SHOW TABLES")
    myresult = cur.fetchall()
    for x in myresult:
        table=x[0]
        print(table)

except mysql.connector.Error as e:
    print(e) 
conn.close()