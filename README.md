# n3rgy
Get data from n3rgy for electrisity and gas and write into a mysql db.

Warning this is not the nicest in anyway shape of form.

Built using Python3.8

tables.sql include the table defs.
get-data.py update with the DB user/password and n3gry auth details.  
run_get_data.sh run from crontab.

For display I used metabase opensource https://www.metabase.com/

config file needs needs to be copied to config.txt and updated with your authentication data for n3rgy and the mysql db

todo: 
* package lists
* build script


