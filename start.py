import uuid
import json
import os

dayMap= {'M':"Monday",'T':"Tuesday",'W':"Wednesday",'R':"Thursday",'F':"Friday",'S':"Saturday",'U':"Sunday"}

def getUserInput():
	q= raw_input('What query string are you interested in?')
	days= raw_input('On which days do you want to receive feedback digest? (Enter M,T,W,R,F,S,U without spaces)')
	emailAddr= raw_input('What is your Microsoft email address?')
	GUID= str(uuid.uuid4())
	return q,days,emailAddr,GUID


def writeToConfigJSON(q,days,emailAddr,GUID): 
	#convert day chars to day strings:
	days= [dayMap[elem] for elem in list(days)]

	#generate json to write to file
	userJson= {GUID:{'query':q, 'days':days, 'emailAddr':emailAddr}}
	writeJSONToFile(GUID, userJson, "config.json")


def writeJSONToFile(GUID, userJson,filename):
	#read in existing JSON
	currentDir= os.getcwd()
	with open(currentDir+'\\'+filename) as data_file:    
		data = json.load(data_file)
	
	#add this GUID into that JSON
	data[GUID]= userJson[GUID]

	#write back into data file
	with open(currentDir+'\\'+filename, 'w') as outfile: 
		json.dump(data, outfile) 


def createTaskXML(daysOfWeek):
	pass

if __name__ == "__main__": 
	q,d,e,g= getUserInput()
	writeToConfigJSON(q,d,e,g)