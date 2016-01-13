#!/usr/bin/python

# Format of each line as:
# city price zestimate history
# history is a list of tuples: (year, price)

import sys
import json
from re import sub

cities = ['San Mateo','Redwood City','Palo Alto',\
          'Mountain View','Santa Clara','San Jose',\
          'Milpitas','Fremont','Menlo Park',\
          'Sunnyvale','Cupertino']
          
pattern = r'[^\d.]'  

def parse_history(history):
    yr = str(history[0].split("/")[-1])
    price_str = sub(pattern,'',history[-1]) if history[-1] else ''
    price = float(price_str) if price_str else None
    return (yr,price)
        
for line in sys.stdin:
    record = json.loads(line)
    city = record["city"]
    if city in cities:
        history_list = record["price_history"]
        history = map(parse_history,history_list)
        if record["status"] == "For Sale":
            price_str = record["price"]
            zestimate_str = record["zestimate"]
            price = float(sub(pattern,'',price_str)) if price_str else None
            zestimate = float(sub(pattern,'',zestimate_str)) if zestimate_str else None
            #some prices listed are not correct so use price history
            if price and zestimate and price < zestimate-200000: 
                if history[0][0] == "15":
                    price = history[0][1]

                else:
                    price = None
        else:
            price = None
            zestimate = None

        print "{0}\t{1}\t{2}\t{3}".format(city,price,zestimate,history)

