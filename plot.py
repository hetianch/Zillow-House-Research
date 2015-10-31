import pickle
import numpy as np
import pandas as pd
from bokeh.io import output_file, show,vplot
from bokeh.charts import Bar
from bokeh.plotting import figure
from bokeh.models import PrintfTickFormatter
import datetime


overprice_count = pickle.load(open('overprice_count.p','r'))
underprice_count = pickle.load(open('underprice_count.p','r'))
median_price = pickle.load(open('median_price.p','r'))

cities = ['San Mateo','Redwood City','Palo Alto',\
		  'Mountain View','Santa Clara','San Jose',\
		  'Milpitas','Fremont']

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
FLAT_COLORS = ['#3498db','#8e44ad','#e67e22','#c0392b','#2ecc71','#1abc9c','#34495e','#f1c40f','#f1a9a0']

output_file("plots.html", title="correlation.py example")

#plot1
p1 = figure(width=850,\
	 plot_height=500,\
	 x_axis_label = "Year",\
	 y_axis_label = "Median Sold Price",\
	 title_text_font_size='14pt',\
	 tools = TOOLS)
p1.title = "Median House Prices Change over Year at Major Silicon Valley Cities"
p1.yaxis[0].formatter = PrintfTickFormatter(format="$%2.1fM")
dates = np.arange(2000,2020)
for i,price in enumerate(median_price):
	if cities[i] == 'Palo Alto': #not enough history data. 
		pass
	else:
		p1.line(dates,map((lambda x: x/10**6),price),color = FLAT_COLORS[i],legend = cities[i],line_width = 2)
p1.legend.orientation = "top_left"
# p1.legend.label_text_size = '10pt'
p1.grid.grid_line_alpha=0.3

#plot2
over_dic = {'city':pd.Series(cities),'numHouse': pd.Series(overprice_count),'overPrice': pd.Series(['over' for _ in xrange(len(cities))])}
under_dic = {'city':pd.Series(cities),'numHouse': pd.Series(underprice_count),'overPrice': pd.Series(['under' for _ in xrange(len(cities))])}

over_df = pd.DataFrame(over_dic)
under_df = pd.DataFrame(under_dic)
df = pd.concat([over_df,under_df],axis=0)

p2 = Bar(df,label = 'city',\
		 values = 'numHouse',\
		 stack='overPrice',\
		 title = "Number of Over VS Under Priced Houses for sale at Major Silicon Valley Cities in 2015",\
		 legend = 'top_right',\
		 xlabel = 'Cities',
		 ylabel = 'Number of Houses',
		 width = 800)

p = vplot(p1,p2)
show(p)
