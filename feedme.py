from scrape import *
from emailer import *
import time
import sys
from selenium.common.exceptions import *

if __name__ == "__main__":
	print "starting program"
	t= time.time()

	try:
		driver= initializeWebDriver()
	except TimeoutException:
		sendEmail({'rows':[]})
		print "Email sent!"
		sys.exit()

	print "Driver initialized", time.time()-t
	t=time.time()

	feedJSON= columnsToJSON(BeautifulSoup(driver.page_source, "html.parser"))
	print "JSONify complete", time.time()-t
	t=time.time()

	sendEmail(feedJSON)
	print "Email sent!", time.time()-t

