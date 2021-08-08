# pw-flights
#Python Weekend Flights Task
# Contact https://github.com/odTbo if you have any problems/questions.

Python script that takes 3 arguments of flights .csv file "example_dataset.csv", origin airport code, example "WUE" and destination airport code, example "JBN".
First argument can be either be filename if it's in the same folder as script or you need to specify the full path to the file.

This script looks for ALL possible combinations of flights until it reaches chosen destination.
It outputs selected flights as JSON format sorted from lowest total price to highest total price.

REQUIREMENTS: Latest version of Python

Csv file of your choice should be in a format as follows:

flight_no,origin,destination,departure,arrival,base_price,bag_price,bags_allowed
ZH151,WIW,ECV,2021-09-01T07:25:00,2021-09-01T12:35:00,245,12,2
ZH665,ECV,RFZ,2021-09-01T12:10:00,2021-09-01T14:40:00,58,12,2
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

HOW TO RUN:
Simply run the script from command line followed by name of your csv file, code of origin airport and code of destination airport.

example:

C:\Program files>python solution.py flights_dataset.csv YOT IUQ
