#!/usr/bin/python3
import requests
import mysql.connector
import datetime
import argparse
import configparser
import math
import json
import solaredge_interface
from solaredge_interface.api.SolarEdgeAPI import SolarEdgeAPI

#smartmeter intervals 00 and 30 
#solaredge intervals 00, 15,30 and 45
#solardege 15 and 30 -> smartmeter 30
#solaredge 45 and 00 -> smartmeter 00

config=configparser.ConfigParser()
config.read("config.txt")

dbtouse=config.get("dbconfig","db")
dbuser=config.get("dbconfig","dbuser")
dbpassword=config.get("dbconfig","dbpasswd")
apikey=config.get("solaredge","apikey")
site=config.get("solaredge","site")
firstgenerationdate=config.get("solaredge","firstgernationdate")

cnx = mysql.connector.connect(user=dbuser, password=dbpassword,
                              host='127.0.0.1',
                              database=dbtouse)

query_cursor = cnx.cursor()
query_cursor.execute("select DATE_FORMAT(max(timestamp), '%Y%m%d') from timestamps where metric='solar_generation'")
timestamp=query_cursor.fetchall()
first_timestamp=timestamp[0][0]
if first_timestamp is None:
    first_timestamp=firstgenerationdate 

first_timestamp=datetime.datetime.strptime(first_timestamp, "%Y%m%d")
end_date=first_timestamp + datetime.timedelta(days=30)
today = datetime.datetime.now()
if end_date>today:
   end_date=today

end_date=end_date.strftime('%Y-%m-%d')
first_timestamp=first_timestamp.strftime('%Y-%m-%d')

cursor = cnx.cursor()

api = SolarEdgeAPI(api_key=apikey, datetime_response=True, pandas_response=False)


response=api.get_site_energy(site,first_timestamp,end_date,"QUARTER_OF_AN_HOUR")
#print(response)

jsonblob = json.loads(response.text)

#print(jsonblob)
jsonblobenergy=jsonblob["energy"]

add_data=("""insert into solaredge (timestamp, solar_generation) values (%s, %s) on duplicate key update solar_generation=%s""")
add_powerdata=("""insert into power_data (timestamp, solar_generation) values (%s, %s) on duplicate key update solar_generation=%s""")
halfhourkwh=0

for value in jsonblobenergy["values"]:
   current_timestamp=value["date"]
   kwh=float(int(0 if value["value"] is None else value["value"]))/1000
   data=(current_timestamp,kwh,kwh)
   cursor.execute(add_data,data)
   #print(current_timestamp) #2023-08-28 00:00:00
   datetime_current = datetime.datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S')
   MINUTE = datetime_current.strftime('%M')  
   #note there is a kind of bug here that if we were producing power over night then the figures would be wrong but as it is dark at midnight there is no issue!
   if MINUTE == '15':
      halfhourkwh=kwh
   if MINUTE == '30':
      halfhourkwh=halfhourkwh+kwh
      power_data=(current_timestamp,halfhourkwh,halfhourkwh)
      cursor.execute(add_powerdata,power_data)
   if MINUTE == '45':
      halfhourkwh=kwh
   if MINUTE == '00':
      halfhourkwh=halfhourkwh+kwh
      power_data=(current_timestamp,halfhourkwh,halfhourkwh)
      cursor.execute(add_powerdata,power_data)

metric='solar_generation'
data_last_timestamp=(metric,current_timestamp,current_timestamp)
add_data_last_timestamp=("""insert into timestamps (metric,timestamp) values (%s, %s) on duplicate key update timestamp=%s""")
cursor.execute(add_data_last_timestamp,data_last_timestamp)
cnx.commit()
cursor.close()
cnx.close()

