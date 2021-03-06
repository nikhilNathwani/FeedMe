import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys
import os

query="share"
startDate="07/01/16"
endDate="07/18/16"
months= {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}

#NOTES:
#--Columns are fixed for now
#--Platforms are fixed for now
#dates formatted as YYYY-MM-DD
def formatQueryURL(query,startDate="",endDate="", usedJSON=False):
	urlBase= 'http://ofeedbackdashboard.cloudapp.net/?#/discover?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),'
	if usedJSON==False:
		time= 'time:(from:\''+startDate+'T04:00:00.000Z\',mode:absolute,to:\''+endDate+'T03:59:59.999Z\'))'
	else: 
		time= 'time:(from:\''+startDate+'Z\',mode:absolute,to:\''+endDate+'Z\'))'
	urlMid= '&_a=(columns:!(comment,product,officeBuild,commentURL),index:feedback,interval:auto,query:(query_string:(analyze_wildcard:!t,'
	q= 'query:\'(comment:%22'+query.replace(' ','%20')+'%22)%20AND%20(product:%22desktop%20word%22%20OR%20%22desktop%20powerpoint%22%20OR%20%22desktop%20excel%22)\')),'
	urlEnd= 'sort:!(submitDate,desc))'
	return urlBase+time+urlMid+q+urlEnd


def formatColumn(i,cols,isFinalCol):
	if not(isFinalCol):
		if i==0:
			date= cols[i].text.encode("ascii","ignore")
			month,DD,YYYY= date[:date.find(',')].split(' ')
			return str(months[month])+"/"+DD[:-2]+'/'+YYYY[-2:]
		return cols[i].text.encode("ascii","ignore")
	else: 
		product, build, url= [elem.text.encode("ascii","ignore") for elem in cols[i:]]
		build= 'n/a' if build==" - " else build
		return product + ", "+build+", <a target=\"_blank\" href="+url+">Comment URL</a>"
	

def columnsToJSON(soup):
	body= soup.find("table",{"class" : "kbn-table"}).find("tbody")
	rows= body.findAll('tr', {"class" : "discover-table-row"})

	#column order: time, comment, product, build, ofeedback url
	json= {'headers':["#","Date", "Comment", "Metadata"], 'rows':[]}
	json['preamble']= {'numFeedback':len(rows),'earliestComment':rows[-1].findAll('td')[1].text.encode("ascii","ignore"),'latestComment':rows[0].findAll('td')[1].text.encode("ascii","ignore")}
	buildHits= {}

	for i,row in enumerate(rows):
		json["rows"].append([str(i+1)]) #add row # in as first column
		cols= row.findAll('td')[1:] #skip over first folumn, which is justa a dropdown button
		numColsAddedToEmail= 3
		
		#add to buildHits dict
		build= cols[3].text.encode("ascii","ignore")
		if build != ' - ':
			buildHits[build] = buildHits.get(build, 0) + 1

		#format columns as json for each row 
		for j in range(numColsAddedToEmail):
			json["rows"][-1].append(formatColumn(j,cols,j==numColsAddedToEmail-1))

	#find max build hits
	json['preamble']['mostCommonBuild']= max(buildHits, key=buildHits.get)
	json['preamble']['maxBuildHits']= buildHits[json['preamble']['mostCommonBuild']]

	#print json['preamble']
	return json
		

def getStartDate(chosenDays):
	dayNums= {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
	
	dayNum= datetime.today().weekday()
	delta= 0
	startDate= ""

	while startDate=="":
		dayNum= (dayNum-1)%7
		delta+= 1
		if dayNums[dayNum] in chosenDays:
			startDate= datetime.now() - timedelta(days=delta)

	return str(datetime.strftime(startDate, '%Y-%m-%dT%H:%M:%S'))+'.000'


#returns the driver
def initializeWebDriver(query="save as", startDate='2016-07-01', endDate='2016-07-22', usedJSON=False):
	driver = webdriver.PhantomJS() 
	driver.get(formatQueryURL(query,startDate,endDate,usedJSON))
	driver.save_screenshot('screenNOWWW.png') # save a screenshot to disk	
	try:
		element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "vis-tooltip")))
	except Exception,e:
		print e
		return ""

	#deal with infinite scroll
	pause=0.1
	lastHeight = driver.execute_script("return document.body.scrollHeight")
	while True:
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    time.sleep(pause)
	    newHeight = driver.execute_script("return document.body.scrollHeight")
	    if newHeight == lastHeight:
	        break
	    lastHeight = newHeight

	driver.save_screenshot('screenAfter.png') # save a screenshot to disk	
	return driver


#add timeouts for these webdriver functions
if __name__ == "__main__":
	print getUserDataFromJSON("119264c7-a420-46d0-8b08-3678aa245f9d")
	sys.exit()

	print "starting program"
	t= time.time()

	driver = webdriver.PhantomJS() # or add to your PATH
	driver.set_window_size(1024, 1768) # optional
	print "shit initialized", time.time()-t
	t= time.time()

	driver.get(formatQueryURL("Save as",'2016-07-15','2016-07-20'))
	element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "vis-tooltip")))	
	print "got url", time.time()-t
	t= time.time()

	driver.save_screenshot('screen1.png') # save a screenshot to disk
	print "got screenshot", time.time()-t

	c= columnsToJSON(BeautifulSoup(driver.page_source, "html.parser"))

