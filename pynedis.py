#!/usr/bin/python3

import http.client
import json
import mysql.connector
from mysql.connector import errors
from environs import Env
import os
import time
from datetime import datetime,timedelta
import itertools


while True:

    print("\n")
    print("                             _ _      ")
    print("                            | (_)     ")
    print("  _ __  _   _ _ __   ___  __| |_ ___  ")
    print(" | '_ \| | | | '_ \ / _ \/ _` | / __| ")
    print(" | |_) | |_| | | | |  __/ (_| | \__ \ ")
    print(" | .__/ \__, |_| |_|\___|\__,_|_|___/ ")
    print(" | |     __/ |                        ")
    print(" |_|    |___/                         ")

    env = Env()
    env.read_env()

    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Getting var env")

    sql_user= str(os.environ.get('SQL_USER'))
    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_USER: "+sql_user)

    sql_password= str(os.environ.get('SQL_PASSWORD'))
    if sql_password == "":
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_PASSWORD is empty")
        break

    else:
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_PASSWORD: *********")

        sql_host= str(os.environ.get('SQL_HOST'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_HOST: "+sql_host)
        sql_db= str(os.environ.get('SQL_DB'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_DB: "+sql_db)
        sql_port= int(os.environ.get('SQL_PORT'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | SQL_PORT: "+str(sql_port))

    try: 
        exec_hour= str(os.environ.get('EXEC_HOUR'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | EXEC HOUR: "+exec_hour)
    except:
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | EXEC HOUR must be like: 00:00:00")
        break

    try: 
        collect_id= str(os.environ.get('COLLECT_ID'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | COLLECT ID: "+collect_id)
    except:
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Please enter your collect ID (available at https://mon-compte-client.enedis.fr/)")
        break

    try: 
        api_token= str(os.environ.get('API_TOKEN'))
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | API TOKEN: *********************** ")
    except:
        print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Please enter your api token (available at https://enedisgateway.tech/)")
        break

    ItsNotTime= True
    while ItsNotTime:
        Now=datetime.now()
        timing = Now.strftime("%H:%M:%S")
        time.sleep(1)
        # print(timing)
        if timing == exec_hour:
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Its time to collect the data ")
            ItsNotTime=False

            DATE_TODAY=datetime.today()
            DATE_YESTERDAY=timedelta(days = 1)
            SEARCH_DATE=DATE_TODAY-DATE_YESTERDAY
            start_date=SEARCH_DATE.strftime("%Y-%m-%d")
            end_date=DATE_TODAY.strftime("%Y-%m-%d")
            
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | Start date: "+str(start_date)+" - End date: "+str(end_date))

            conn = http.client.HTTPSConnection("enedisgateway.tech")
            payload = {'type': 'consumption_load_curve','usage_point_id': collect_id,'start': start_date,'end': end_date}
            headers = {'Authorization': api_token,'Content-Type': "application/json",}
            conn.request("POST", "/api", json.dumps(payload), headers)
            res = conn.getresponse()
            data = res.read()
            decoded_data=data.decode("utf-8")

            json_response=json.loads(decoded_data)
            try:
                metric_only=json_response["meter_reading"]["interval_reading"]

            except KeyError():
                time.sleep(20)
                conn = http.client.HTTPSConnection("enedisgateway.tech")
                payload = {'type': 'consumption_load_curve','usage_point_id': collect_id,'start': start_date,'end': end_date}
                headers = {'Authorization': api_token,'Content-Type': "application/json",}
                conn.request("POST", "/api", json.dumps(payload), headers)
                res = conn.getresponse()
                data = res.read()
                decoded_data=data.decode("utf-8")
                json_response=json.loads(decoded_data)
                metric_only=json_response["meter_reading"]["interval_reading"]

            conn = mysql.connector.connect(user=sql_user,password=sql_password,host=sql_host,database=sql_db,port=sql_port,auth_plugin='mysql_native_password')
            cur = conn.cursor()

            for row_value in metric_only:
                metric_date=row_value["date"]
                metric_date=str(metric_date)
                date_time_obj = datetime.strptime(metric_date, '%Y-%m-%d %H:%M:%S')
                converted_date= date_time_obj - timedelta(hours=1)
                print(converted_date)
                metric_value=row_value["value"]

                sql_request="INSERT into enedis_metrics (time,metric,conso_watt) VALUES ('"+str(converted_date)+"','consumption_curve',"+str(metric_value)+")"

                try:
                    cur.execute(sql_request)
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query successfull")
                    conn.commit()

                except mysql.connector.Error as e:
                    print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | INSERT query failed !!")
                    print(e)

            conn.close()
            print("["+datetime.now().strftime("%d/%m/%Y - %H:%M:%S")+"] | ## COLLECT FINISHED ##")
