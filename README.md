# n3rgy and solaredge

All below needs to be rewritten! 

Get data from n3rgy for electrisity and gas and write into a mysql db.

Warning this is not the nicest in anyway shape of form.

Built using Python3.8

usage: get_n3rgy_data.py [-h] metric inout

positional arguments:
  metric      gas electricity
  inout       consumption production

optional arguments:
  -h, --help  show this help message and exit


tables.sql - include the table defs.
get_n3rgy_data.py - script that gets the data
run_get_data.sh - run from crontab.

For display I used metabase opensource https://www.metabase.com/

config file needs needs to be copied to config.txt and updated with your authentication data for n3rgy and the mysql db

I run this from /etc/contab using the following:
2 5    * * *   user  /home/nbooth/n3rgy/run_get_data.sh

or from a user crontab:
2 5    * * *   /home/nbooth/n3rgy/run_get_data.sh

The data from n3rgy is always delayed and not real time. This consumer services is provided to us for free hence please be considereate and choose a diffrent offset from the top of the hour. 

When running a service that has hourly data there is a habbit for people to all query on the hour which drives massive load into the system and increases the costs of the provider. This then leads to the service becoming chargeable or been withdrawn. I don't know if this will happen in this case (as I have nothing to do with n3rgy) but Please be considerate to their costs with how you run this. 

The script will get ALL data it has not got before with a max window of 90 days. If you don't look at the data often maybe run the script manually when you need to get it updated. Or if a daily refresh is ok then do a daily refresh. The example crontab runs at 5.02am once a day for example.

todo: 
*   package lists
*   build script
