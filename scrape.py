import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0



if __name__ == "__main__":
	driver = webdriver.PhantomJS() # or add to your PATH
	driver.set_window_size(1024, 1768) # optional
	driver.get('http://ofeedbackdashboard.cloudapp.net/?#/discover/Detailed-Feedback?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:now-30d,mode:quick,to:now))&_a=(columns:!(officeBuild,product,comment,isInternal,oSUserLocale,commentURL),filters:!((exists:(field:product),meta:(disabled:!f,index:feedback,key:exists,negate:!f,value:product))),index:feedback,interval:auto,query:(query_string:(analyze_wildcard:!t,query:\'(comment:%22chat%22)%20AND%20(product:%22desktop%20word%22%20OR%20%22desktop%20powerpoint%22%20%20OR%20%22desktop%20excel%22)\')),sort:!(product,asc))')
	element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "vis-tooltip")))
	driver.save_screenshot('screen4.png') # save a screenshot to disk