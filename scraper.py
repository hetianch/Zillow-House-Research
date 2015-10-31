import json
import urllib2
import re
import pickle
from scrapezillow.scraper import scrape_url
import time

#initialize
numPages = 2887
url_prefix = "http://www.zillow.com/search/GetResults.htm?spt=homes&status=100000&lt=111001&ht=100000&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0&zoom=4&rect=-135087891,31334871,-103491211,43052833&p="
url_postfix = "&sort=featured&search=maplist&disp=1&rid=9&rt=2&listright=true&isMapSearch=1&zoom=4"
request_timeout = 0.3
out_file_pre = "results"
out_file_post = ".json"

results = []

for pageNum in range(1,numPages+1):

	url = url_prefix + str(pageNum) + url_postfix 

	zpidSource = json.load(urllib2.urlopen(url))['list']['listHTML']
	zpids = re.findall(r'id="zpid_(\d{8})"',zpidSource)

	for i,zpid in enumerate(zpids):
		try:
	 		results.append(scrape_url(None, int(zpid), request_timeout))
	 		time.sleep(0.5)
	 		print i, 'out of', len(zpids)
	 	except:
	 		pass

	print 'finish scraping page %d,%d houses found!' %(pageNum,len(zpids))

with open(out_file,'w') as f:
 	json.dump(results,f)