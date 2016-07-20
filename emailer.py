import smtplib 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def constructEmail(feedJSON):
	if len(feedJSON['rows'])==0:
		return """\
		<html>
			<head></head>
			<body>
				<p>There is no Desktop Office W/X/P send-a-smile feedback matching \'""" + feedJSON['params']['query'] + """\' within the specified time interval. If you believe you're seeing this in error, please contact <a href=\"mailto:nikhilna@microsoft.com\">Nikhil</a>.</p>
			</body>
		</html>
		"""

	htmlStart= """\
		<html>
			<head>
				<style type="text/css">
					table {
					  border-collapse: collapse;
					  font-family: Segoe UI, sans-serif;
					}
					td, th {
					  border: 1px solid #999;
					  padding: 0.5rem;
					  text-align: left;
					}
					thead {
						background-color: #94B6D2;
					}
				</style>
			</head>
			<body>
		"""
	p= feedJSON['preamble']
	num, early, late, build, hits= str(p["numFeedback"]), p["earliestComment"], p["latestComment"], p["mostCommonBuild"], str(p["maxBuildHits"])
	preamble= "<strong># Comments: </strong>" + num + "<br><strong>Earliest comment: </strong>" + early + "<br><strong>Latest comment: </strong>" + late + "<br><strong>Most common build: </strong>" + build + " (" + hits + " hits)"

	htmlEnd= """\
					</tbody>
				</table>
			</body>
		</html>
		"""

	table= "<table><thead><tr>"
	for header in feedJSON['headers']:
		table+= "<th>"+header+"</th>"
	table+= "</tr></thead><tbody>"

	for i,row in enumerate(feedJSON['rows']):
		
		table+= "<tr "
		if i%2==0:
			table += "style=\"background-color: #DCE5EE;\""
		table+= ">"

		for col in row:
			table+= "<td>" + col + "</td>"
		table+= "</tr>"

	return htmlStart+preamble+table+htmlEnd


#params has 'query' and 'emailAddr'
def sendEmail(feedJSON, params):
	#sender and recipient
	me= "DocsTest1@docse3testtenant.onmicrosoft.com"
	you= params['emailAddr']

	#message container
	msg= MIMEMultipart('alternative')
	msg['Subject']= "Your Latest \'"+ params['query'] + "\' Feedback is Ready"
	msg['From']= me
	msg['To']= you

	#message body 
	html= constructEmail(feedJSON)
	#print "Completed writing email!"

	#Record MIME types of both parts
	part= MIMEText(html,'html')
	msg.attach(part)
	#print "Attached to container!"

	#send message via local SMTP server
	mail = smtplib.SMTP('smtp.office365.com', 587)

	mail.starttls()

	mail.login(me, 'Password!!')
	mail.sendmail(me, you, msg.as_string())
	mail.quit()


if __name__ == "__main__":
	sendEmail("")
