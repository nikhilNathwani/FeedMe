import uuid
import json
from datetime import datetime
import os

dayMap= {'M':"Monday",'T':"Tuesday",'W':"Wednesday",'R':"Thursday",'F':"Friday",'S':"Saturday",'U':"Sunday"}

def getUserInput():
	q= raw_input('What query string are you interested in?')
	days= raw_input('On which days do you want to receive feedback digest? (Enter M,T,W,R,F,S,U without spaces)')
	emailAddr= raw_input('What is your Microsoft email address?')
	GUID= str(uuid.uuid4())
	return q,days,emailAddr,GUID

def getDays(dayChars):
	return [dayMap[elem] for elem in list(dayChars)]

def writeToConfigJSON(q,days,emailAddr,GUID): 
	#convert day chars to day strings:
	days= getDays(days)

	#generate json to write to file
	userJson= {GUID:{'query':q, 'days':days, 'emailAddr':emailAddr}}
	writeJSONToFile(GUID, userJson, "config.json")


def writeJSONToFile(GUID, userJson, filename):
	#read in existing JSON
	currentDir= os.getcwd()
	with open(currentDir+'\\'+filename) as data_file:    
		data = json.load(data_file)
	
	#add this GUID into that JSON
	data[GUID]= userJson[GUID]

	#write back into data file
	with open(currentDir+'\\'+filename, 'w') as outfile: 
		json.dump(data, outfile) 

	return data


def createTaskXML(days,GUID):
	days= getDays(days)
	now= datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')

	xml= """<?xml version="1.0" encoding="UTF-16"?>
		<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
		  <RegistrationInfo>
		    <Date>"""
	xml+= now+".000000"
	xml+= """</Date>
		    <Author>nikhilna</Author>
		    <URI>\FeedMe</URI>
		  </RegistrationInfo>
		  <Triggers>
		    <CalendarTrigger>
		      <StartBoundary>"""
	
	xml+= datetime.strftime(datetime.now(), '%Y-%m-%d')+'T05:00:00'

	xml+="""</StartBoundary>
		      <ExecutionTimeLimit>PT4H</ExecutionTimeLimit>
		      <Enabled>true</Enabled>
		      <ScheduleByWeek>
		        <DaysOfWeek>"""

	for day in days:
		xml+= "<"+day+" />"

	xml+= """</DaysOfWeek>
		        <WeeksInterval>1</WeeksInterval>
		      </ScheduleByWeek>
		    </CalendarTrigger>
		  </Triggers>
		  <Principals>
		    <Principal id="Author">
		      <UserId>S-1-5-21-124525095-708259637-1543119021-1464612</UserId>
		      <LogonType>Password</LogonType>
		      <RunLevel>HighestAvailable</RunLevel>
		    </Principal>
		  </Principals>
		  <Settings>
		    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
		    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
		    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
		    <AllowHardTerminate>true</AllowHardTerminate>
		    <StartWhenAvailable>true</StartWhenAvailable>
		    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
		    <IdleSettings>
		      <StopOnIdleEnd>false</StopOnIdleEnd>
		      <RestartOnIdle>false</RestartOnIdle>
		    </IdleSettings>
		    <AllowStartOnDemand>true</AllowStartOnDemand>
		    <Enabled>true</Enabled>
		    <Hidden>false</Hidden>
		    <RunOnlyIfIdle>false</RunOnlyIfIdle>
		    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
		    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
		    <WakeToRun>true</WakeToRun>
		    <ExecutionTimeLimit>PT72H</ExecutionTimeLimit>
		    <Priority>7</Priority>
		  </Settings>
		  <Actions Context="Author">
		    <Exec>
		      <Command>C:\Users\\nikhilna\Documents\GitHub\FeedMe\\feedme.py</Command>
		      <Arguments>"""
	xml+= GUID
	xml+="""</Arguments>
			<WorkingDirectory>C:\Users\\nikhilna\Documents\GitHub\FeedMe\</WorkingDirectory>
		    </Exec>
		  </Actions>
		</Task>
		"""	

	#write to file
	currentDir= os.getcwd()
	with open(currentDir+'\\tasks\\'+GUID+'.xml', "w")  as taskFile:    
		taskFile.write(xml)



if __name__ == "__main__": 
	q,d,e,g= getUserInput()
	j= writeToConfigJSON(q,d,e,g)
	createTaskXML(d,g)