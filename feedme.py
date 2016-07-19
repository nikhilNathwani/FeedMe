from scrape import *
from emailer import *
import time

if __name__ == "__main__":
	print "starting program"
	t= time.time()

	driver= initializeWebDriver()
	print "Driver initialized", time.time()-t
	t=time.time()

	feedJSON= columnsToJSON(BeautifulSoup(driver.page_source, "html.parser"))
	print "JSONify complete", time.time()-t
	t=time.time()

	print feedJSON
	sendEmail(feedJSON)
	print "Email sent!", time.time()-t

