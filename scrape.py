import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup

query="save as"
startDate="07/01/16"
endDate="07/18/16"

#returns user's query string and time interval
def getUserInput():
	pass


#NOTES:
#--Columns are fixed for now
#--Platforms are fixed for now
#dates formatted as YYYY-MM-DD
def formatQueryURL(query,startDate="",endDate=""):
	urlBase= 'http://ofeedbackdashboard.cloudapp.net/?#/discover?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),'
	time= 'time:(from:\''+startDate+'T04:00:00.000Z\',mode:absolute,to:\''+endDate+'T03:59:59.999Z\'))'
	urlMid= '&_a=(columns:!(comment),index:feedback,interval:auto,query:(query_string:(analyze_wildcard:!t,'
	q= 'query:\'(comment:%22'+query.replace(' ','%20')+'%22)%20AND%20(product:%22desktop%20word%22%20OR%20%22desktop%20powerpoint%22%20OR%20%22desktop%20excel%22)\')),'
	urlEnd= 'sort:!(submitDate,desc))'
	return urlBase+time+urlMid+q+urlEnd


def getCommentColumn(soup):
	body= soup.find("table",{"class" : "kbn-table"}).find("tbody")
	rows= body.findAll('tr', {"class" : "discover-table-row"})
	comments= []
	for row in rows:
		c= row.findAll('td')[-1].text
		comments.append(c)
	return column



#add timeouts for these webdriver functions
if __name__ == "__main__":
	print "starting program"
	t= time.time()

	driver = webdriver.PhantomJS() # or add to your PATH
	driver.set_window_size(1024, 1768) # optional
	print "shit initialized", time.time()-t
	t= time.time()

	driver.get(formatQueryURL("Save as",'2016-07-15','2016-07-20'))
	element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "vis-tooltip")))	
	print "got url", time.time()-t
	t= time.time()

	driver.save_screenshot('screen1.png') # save a screenshot to disk
	print "got screenshot", time.time()-t

	getCommentColumn(BeautifulSoup(driver.page_source, "html.parser"))


