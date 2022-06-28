#!/usr/local/python-3.8.9/bin/bin/python3
import requests, json
import mysql.connector
import datetime
import argparse
import configparser


config=configparser.ConfigParser()
config.read("config.txt")

dbtouse=config.get("dbconfig","db")
dbuser=config.get("dbconfig","dbuser")
dbpassword=config.get("dbconfig","dbpasswd")
n3rgysecret=config.get("n3rgy","secret")

headers= {'Authorization': n3rgysecret}

argparser = argparse.ArgumentParser()
argparser.add_argument("metric", type=str, default="electricity", help="gas electricity")
argparser.add_argument("db", type=str, default="power", help="DB Name")
args = argparser.parse_args()

metric=args.metric
dbtouse=args.db
cnx = mysql.connector.connect(user=dbuser, password=dbpassword,
                              host='127.0.0.1',
                              database=dbtouse)

query_cursor = cnx.cursor()
#try:
#query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from smartmeter_consumption");
if metric=="gas":
   query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from smartmeter_last_timestamps where metric='gas'")
if metric=="electricity":
   query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from smartmeter_last_timestamps where metric='electricity'")


timestamp=query_cursor.fetchall()
first_timestamp=timestamp[0][0]
if first_timestamp is None:
    first_timestamp="20210530"

end_date=datetime.datetime.strptime(first_timestamp, "%Y%m%d") + datetime.timedelta(days=90)
end_date=end_date.strftime('%Y%m%d')


url = "https://consumer-api.data.n3rgy.com/"+metric+"/consumption/1?start="+first_timestamp+"&end="+end_date
r=requests.get(url,headers=headers)
jsondata=r.json()
r.close()


cursor = cnx.cursor()


if metric=="gas":
   add_data=("""insert into smartmeter_consumption (timestamp, gas) values (%s, %s) on duplicate key update gas=%s""")

if metric=="electricity":
   add_data=("""insert into smartmeter_consumption (timestamp, electricity) values (%s, %s) on duplicate key update electricity=%s""")

for value in jsondata["values"]:
    current_timestamp= datetime.datetime.strptime(value["timestamp"], '%Y-%m-%d %H:%M')
    data=(current_timestamp,value["value"],value["value"])
    cursor.execute(add_data,data)
add_data_last_timestamp=("""insert into smartmeter_last_timestamps (metric,timestamp) values (%s, %s) on duplicate key update timestamp=%s""")
data_last_timestamp=(metric,current_timestamp,current_timestamp)
cursor.execute(add_data_last_timestamp,data_last_timestamp)   

cnx.commit()
cursor.close()


cnx.close()

