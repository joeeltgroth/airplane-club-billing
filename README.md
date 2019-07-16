# airplane-club-billing
Tool for building flying club invoices


## Virtual Environment Info
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Create the input files
Sample csv data files are in the data directory.
Purpose of each: 
 - club.csv: Addresses for the club
 - pilot.csv: Pilot data such as name address, previous balance. 
 - pilot_log.csv: Log of the last month's flying
 - plane.csv: airplane ids and their hourly rate. 

## Run it
```
$ python main.py
```

## What to expect
A pdf invoice file will be created (in the output directory) for 
each pilot in data/pilot.csv. 


### References
 - FPDF Library: http://fpdf.org/
 - Python environment manager: https://github.com/pyenv/pyenv
 - Virtual Environments: https://virtualenv.pypa.io/en/latest/
 - Pip Requirements: https://pip.pypa.io/en/stable/user_guide/
 - Various techniques: https://stackoverflow.com
 - Dates: https://www.w3schools.com/python/python_datetime.asp
 - Currency: https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
 
 