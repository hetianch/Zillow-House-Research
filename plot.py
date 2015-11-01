import pickle
import numpy as np
import pandas as pd
from bokeh.io import output_file, show,vplot
from bokeh.charts import Bar
from bokeh.plotting import figure
from bokeh.embed import components 
from bokeh.models import PrintfTickFormatter
from jinja2 import Template
import webbrowser
import datetime
import os 
import six


overprice_count = pickle.load(open('overprice_count.p','r'))
underprice_count = pickle.load(open('underprice_count.p','r'))
median_price = pickle.load(open('median_price.p','r'))


cities = ['San Mateo','Redwood City','Palo Alto',\
		  'Mountain View','Santa Clara','San Jose',\
		  'Milpitas','Fremont','Menlo Park',\
		  'Sunnyvale','Cupertino']

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
FLAT_COLORS = ['#3498db','#8e44ad','#e67e22','#c0392b','#2ecc71','#1abc9c','#34495e','#f1c40f','#f1a9a0','#43353d','#888888','#9e906e']

#plot1
p1 = figure(width=850,\
	 plot_height=500,\
	 x_axis_label = "Year",\
	 y_axis_label = "Median Sold Price",\
	 title_text_font_size='14pt',\
	 tools = TOOLS)
p1.title = "Median House Prices Change over Year at Selected Silicon Valley Cities"
p1.yaxis[0].formatter = PrintfTickFormatter(format="$%2.1fM")
dates = np.arange(2000,2020)
selected = ["Menlo Park","Mountain View", "Sunnyvale","Cupertino","Milpitas","Fremont"]
for i,price in enumerate(median_price):
	if cities[i] in selected:
		p1.line(dates,map((lambda x: x/10**6),price),color = FLAT_COLORS[i%8],legend = cities[i],line_width = 2)
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

plots = {1:p1,2:p2}
for i,p in plots.items():
	script, div = components(p)
	template = Template('''<!DOCTYPE html>
	<html>
	  <head>
	    <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.2.min.css" type="text/css" />
	    <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.2.min.js"></script>
	    {{ script | safe }}
	  </head>
	  <body>
	    <div class=page>
	      <h1>Zillow-House-Research Project Plot {{i}}</h1>
	      {{ div | safe }}
	    </div>
	  </body>
	</html>
	''')

	html_file = 'plot%d.html'%(i)
	with open(html_file, 'w') as textfile:
	    textfile.write(template.render(script=script, div=div,i=i))

#url = 'file:{}'.format(six.moves.urllib.request.pathname2url(os.path.abspath(html_file)))
#webbrowser.open(url)

# if __name__=="__main__":
# 	app.run(port=33507)

