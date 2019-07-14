# airplane-club-billing
Tool for building flying club invoices


## Virtual Environment Info
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt

## Create the input files
Sample csv data files are in the data directory.
Purpose of each: 
 - club.csv: Addresses for the club
 - pilot.csv: Pilot data such as name address, previous balance. 
 - pilot_log.csv: Log of the last month's flying
 - plane.csv: airplane ids and their hourly rate. 

## Run it
$ python build_invoices.py

## What to expect
A pdf file will be created for each pilot in data/pilot.csv. 

