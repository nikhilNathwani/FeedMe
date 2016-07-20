from scrape import *
from emailer import *
import time

if __name__ == "__main__":
	t= time.time()
	q= raw_input('What query string are you interested in?')
	emailAddr= raw_input('What is your Microsoft email address?')
	print "Got it. This will take about 20 seconds..."

	driver= initializeWebDriver(q)
	#print "Driver initialized", time.time()-t
	t=time.time()

	feedJSON= columnsToJSON(BeautifulSoup(driver.page_source, "html.parser"))
	#print "JSONify complete", time.time()-t
	t=time.time()

	sendEmail(feedJSON,emailAddr)
	print "Email sent!"#, time.time()-t

