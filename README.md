Zillow House Research Proposal
Hetian Chen, Oct 31 2015

Motivation:
Buying a house is a once-in-a-lifetime investment for many people. A good house not only make a comfortable home but also increase the value of your property over time. Location, Convenience, Safety, Education, Affordability, etc. -- there're too many factors to consider, which make the decision really hard. You need advice, you need information, you need checks and balance. That's the reason why Real Estate Websites like Zillow, Trulia, Redfin, etc. are becoming more and more popular. We can find detailed information about one house, but what we may also care about is: can we buy a similar house with cheaper price at another city? Is it a good time to buy a house now or next year? Are the houses in this city more likely to be over-priced than the nearby city? These interesting questions make it worthwhile and potentially profitable to spend time on. 

Methods:
1) get data:
First of all,the unique identifier(zpid) of 72173 houses at California was obtained by scraping the Zillow website. Then these zpids were used to retrieve information of each house by Zillow API. The information include: address, post-code, listed price, tax history, price estimate (zestimate), house dimensions, etc. 

2) exploratory data analysis:
As an example, I focused on the analysis of houses at major silicon valley cities this time. First of all, data cleaning is performed to exclude obviously mis-recorded house prices. (e.g Listed for sale at $100,00 but was previously bought with more than a million) Second, Median history house prices of each city from 2000 to 2015 are computed to compare the trend of housing price at each city. Finally, number of over-priced and under-priced houses were counted at each city to give an insight about potential real estate speculation. Please note that the reasonable house prices are assumed to be close to house price estimated by Zillow (zestimate)

3) future plan:
With given data, many more interesting analysis and modeling can be performed in the future. For example, Zillow can show you "comparable houses" when you search for one house. However, these "comparable houses" are all from the region you searched. From the exploratory analysis, we know that prices from different regions are quite different, which make it reasonable to search for "comparable houses" at other nearby cities. Given house dimension, number of beds/baths, nearby school ratings, etc, the most easy and brute force way is to run a K nearest neighbor algorithm to find comparable houses at other given cities.

Results:
# embed plot1
The above plot shows the median house prices at 7 cities in silicon valley from 2000 to 2015. We can see that the house prices at Mountain view goes up dramatically after Google founded(1998), and goes down after 2007-2008 financial crisis. Now the median price at Mountain View are about to reach the highest point in history. Besides Mountain View, house prices at all other cities are higher or close to that before financial crisis. As two nearby cities, house prices at Sunnyvale were greatly lower than Mountain view before 2010. However, housing at Sunnyvale gets hotter and hotter after that.This observation is consistent with the fact that people who are scared by the price of Mountain View and Cupertino have started to move to Sunnyvale. Property market speculation is probably another reason. Many houses in Sunnyvale were bought around 300K at 2014 but listed around 800K at 2015, which doubled the price. This further justify our speculation. 

# embed plot2
The above plot shows the number of over vs under priced houses for sale at major silicon valley cities in 2015. As two biggest cities,Fremont and San Jose have the most houses to sale. As three nearby cities, Cupertino has the least percentage of over priced houses than Mountain View and Sunnyvale. Among all cities, the percentage of over-priced houses at Palo Alto is highest. This is consistent with the fact that Palo Alto is close to Sanford, and also is the top school district. 




