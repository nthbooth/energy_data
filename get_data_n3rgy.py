#!/usr/bin/python3
import requests
import mysql.connector
import datetime
import argparse
import configparser
import math

config=configparser.ConfigParser()
config.read("config.txt")

dbtouse=config.get("dbconfig","db")
dbuser=config.get("dbconfig","dbuser")
dbpassword=config.get("dbconfig","dbpasswd")
n3rgysecret=config.get("n3rgy","secret")
n3rgymoveindate=config.get("n3rgy","moveindate")
n3rgyproductionstartdate=config.get("n3rgy","productionstartdate")
headers= {'Authorization': n3rgysecret}

volume_correction=config.get("gas","volume_correction")
calorific_value=config.get("gas","calorific_value")
joules_conversion=config.get("gas","joules_conversion")


argparser = argparse.ArgumentParser()
argparser.add_argument("metric", type=str, default="electricity", help="gas electricity")
argparser.add_argument("inout", type=str, default="consumption", help="consumption production")
#argparser.add_argument("db", type=str, default="power", help="DB Name")
args = argparser.parse_args()

metric=args.metric
inout=args.inout
#dbtouse=args.db
cnx = mysql.connector.connect(user=dbuser, password=dbpassword,
                              host='127.0.0.1',
                              database=dbtouse)

query_cursor = cnx.cursor()

if metric=="gas":
   query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from timestamps where metric='gas'")

if metric=="electricity":
   if inout=="production":
      query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from timestamps where metric='electricity_export'")

if metric=="electricity":
   if inout=="consumption":
      query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from timestamps where metric='electricity'")



timestamp=query_cursor.fetchall()
first_timestamp=timestamp[0][0]
if first_timestamp is None:
   if inout=="consumption":
      first_timestamp=n3rgymoveindate

if first_timestamp is None:
   if inout=="production":
      first_timestamp=n3rgyproductionstartdate

end_date=datetime.datetime.strptime(first_timestamp, "%Y%m%d") + datetime.timedelta(days=90)
end_date=end_date.strftime('%Y%m%d')


url = "https://consumer-api.data.n3rgy.com/"+metric+"/"+inout+"/1?start="+first_timestamp+"&end="+end_date
r=requests.get(url,headers=headers)
jsondata=r.json()
r.close()

#print(url)
cursor = cnx.cursor()


if metric=="gas":
   add_data=("""insert into power_data (timestamp, gas) values (%s, %s) on duplicate key update gas=%s""")
   add_data_kwh=("""insert into power_data (timestamp, gas_kwh) values (%s, %s) on duplicate key update gas_kwh=%s""")

if metric=="electricity":
   if inout=="consumption":
      add_data=("""insert into power_data (timestamp, electricity) values (%s, %s) on duplicate key update electricity=%s""")

if metric=="electricity":
   if inout=="production":
      add_data=("""insert into power_data (timestamp, electricity_export) values (%s, %s) on duplicate key update electricity_export=%s""")

#electricity_production
#print(jsondata);
###there is a bug where n3rgy reports 16777.215 instad of the actual value this is actually a meter error and hence this is not valid data. (gas only)
#'value': 16777.215},

for value in jsondata["values"]:
    current_timestamp=datetime.datetime.strptime(value["timestamp"], '%Y-%m-%d %H:%M')
    data=(current_timestamp,value["value"],value["value"])
    if metric=="gas":
       if math.isclose(value["value"],16777.215):
          gaskwh_data=(current_timestamp,0,0)
          data=(current_timestamp,0,0)
          cursor.execute(add_data,data)
          cursor.execute(add_data_kwh,gaskwh_data)
       else:
          gaskwh=float(value["value"])*float(volume_correction)*float(calorific_value)/float(joules_conversion)
          gaskwh_data=(current_timestamp,gaskwh,gaskwh)
          cursor.execute(add_data,data)
          cursor.execute(add_data_kwh,gaskwh_data)
    else:
       cursor.execute(add_data,data)


    add_data_last_timestamp=("""insert into timestamps (metric,timestamp) values (%s, %s) on duplicate key update timestamp=%s""")

if inout=="consumption":
    data_last_timestamp=(metric,current_timestamp,current_timestamp)
if inout=="production":
    data_last_timestamp=("electricity_export",current_timestamp,current_timestamp)

cursor.execute(add_data_last_timestamp,data_last_timestamp)

cnx.commit()
cursor.close()


cnx.close()

