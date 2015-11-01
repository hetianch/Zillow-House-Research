import json
import pickle
import numpy as np
from re import sub
from decimal import Decimal

global pattern
pattern = r'[^\d.]'


def parse_data(path,cities):
	with open(path,'r') as f:
		data = json.load(f)

	for i,entry in enumerate(data):
		city = data[i]['city']
		if city in cities:
			history_list = data[i]["price_history"]
			history = map(parse_history,history_list)

			if data[i]["status"] == "For Sale":
				price_str = data[i]["price"]
				zestimate_str = data[i]["zestimate"]
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

			yield city,price, zestimate, history

def parse_history(history):
	yr = history[0].split("/")[-1]
	price_str = sub(pattern,'',history[-1]) if history[-1] else ''
	price = float(price_str) if price_str else None
	return (yr,price)

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
	return flat_list

def price_count(path,cities):
	num_cities = len(cities)
	overprice_count = [0]* num_cities
	underprice_count = [0]* num_cities

	for city,price, zestimate, history in parse_data(path,cities):
		if price and zestimate is not None:
			idx = cities.index(city)
			if price > zestimate:
				overprice_count[idx] +=1
			else:
				underprice_count[idx] +=1

	return overprice_count,underprice_count


def price_by_year(path,cities):
	num_cities = len(cities)
	price_list = [[[] for s in xrange(16)] for x in xrange(num_cities)]
	for city,price, zestimate, history in parse_data(path,cities):
		idx = cities.index(city)
		for (yr,pr) in history:
			if 0 <= int(yr) <= 15:
				price_list[idx][int(yr)].append(pr)

	median_price = map(parse_price,price_list)

	return median_price


if __name__ == "__main__":
	cities = ['San Mateo','Redwood City','Palo Alto',\
			  'Mountain View','Santa Clara','San Jose',\
			  'Milpitas','Fremont','Menlo Park',\
			  'Sunnyvale','Cupertino']
			  
	path = "results_MajorCity.json"
	overprice_count,underprice_count = price_count(path,cities)	
	median_price = price_by_year(path,cities)
	pickle.dump(overprice_count,open('overprice_count.p','w'))
	pickle.dump(underprice_count,open('underprice_count.p','w'))
	pickle.dump(median_price,open('median_price.p','w'))	  


