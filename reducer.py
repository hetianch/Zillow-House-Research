#!/usr/bin/python

# Key: city, Val: price zestimate history

import sys
import numpy as np
import re
from decimal import Decimal

pattern = r'[^\d.]'
old_city = None
overprice_count = 0 
underprice_count=0
price_list = [[] for s in xrange(16)]

def parse_price(price):
    flat_list = []
    for i in xrange(len(price)):
        price_year = np.array(price[i], dtype=np.float)
        price_median = np.median(price_year[~np.isnan(price_year)])
        flat_list.append(price_median)

    #data imputation for smooth ploting purpose
    flat_list = np.array(flat_list)
    mask = np.isnan(flat_list)
    flat_list[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), flat_list[~mask])
    
    return flat_list.tolist()

def ext_pattern(string):
    pat = r"\('([0-9]+)',[\s+](\d+\.\d+)\)"
    ext = re.findall(pat,string)
    result = [(int(yr),float(pr)) for yr, pr in ext]
    return result

def string_to_float(string):
    ext = re.sub(pattern,'',string)
    result = float(ext) if ext else None
    return result


for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    
    if len(data_mapped) !=4:
        continue

    city = data_mapped[0]
    price_str = data_mapped[1]
    zestimate_str = data_mapped[2]

    price = string_to_float(price_str)
    zestimate = string_to_float(zestimate_str)
    history = ext_pattern(data_mapped[3])

    if old_city and old_city != city:
        # summerize
        median_price = parse_price(price_list)
        print "{0}\t{1}\t{2}\t{3}".format(old_city,overprice_count,underprice_count,median_price)
        
        # initialize
        overprice_count = 0 
        underprice_count=0
        price_list = [[] for s in xrange(16)]
    
    old_city = city

    if price and zestimate is not None:
        if price > zestimate:
            overprice_count +=1
        else:
            underprice_count+=1

    for (yr,pr) in history:
        if 0 <= yr <= 15:
            price_list[yr].append(pr)

if old_city != None:
    median_price = parse_price(price_list)
    print "{0}\t{1}\t{2}\t{3}".format(city,overprice_count,underprice_count,median_price)








