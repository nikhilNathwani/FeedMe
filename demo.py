from scrape import *
from emailer import *
import time
from selenium.common.exceptions import *
import sys

if __name__ == "__main__":
	t= time.time()
	q= raw_input('What query string are you interested in?')
	emailAddr= raw_input('What is your Microsoft email address?')
	print "Got it. This will take about 20 seconds..."

	try:
		driver= initializeWebDriver(q)
	except TimeoutException:
		sendEmail({'rows':[],'params':{'query':q}})
		print "Email sent!"
		sys.exit()

	feedJSON= columnsToJSON(BeautifulSoup(driver.page_source, "html.parser"))
	#print "JSONify complete", time.time()-t
	#t=time.time()

	sendEmail(feedJSON,{'query':q, 'emailAddr':emailAddr})
	print "Email sent!"#, time.time()-t

