from scrape import *
from emailer import *
import time
import sys
from selenium.common.exceptions import *

def getUserDataFromJSON(guid):
	#read in existing JSON
	currentDir= os.getcwd()
	with open(currentDir+'\\config.json') as data_file:    
		data = json.load(data_file)

	userJSON= data[guid]
	query= userJSON["query"].encode("ascii","ignore")
	startDate= getStartDate(userJSON['days'])
	endDate= str(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S'))+'.000'
	emailAddr= userJSON["emailAddr"].encode("ascii","ignore")

	return query, startDate, endDate, emailAddr


#REMEBER TO CHANGE THE HARD-CODED 'save as' BELOW!!!!
#And should move the try/except into a function, so I don't have to keep copying it over between main methods
if __name__ == "__main__":
	if len(sys.argv)>1:
		guid= sys.argv[1]
	else:
		print "didn't receive GUID"
		sys.exit()

	print "starting program"
	t= time.time()

	query,startDate,endDate,emailAddr= getUserDataFromJSON(guid)

	driver= initializeWebDriver(query, startDate, endDate, True)
	if driver=="":
		sys.exit()

	print "Driver initialized", time.time()-t
	t=time.time()

	feedJSON= columnsToJSON(BeautifulSoup(driver.page_source, "html.parser"))
	print "JSONify complete", time.time()-t
	t=time.time()

	sendEmail(feedJSON,{'query':query,'emailAddr':emailAddr})
	print "Email sent!", time.time()-t

