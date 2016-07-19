import smtplib 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def constructEmail(feedJSON):
	htmlStart= """\
		<html>
			<head></head>
			<body>
				<p>Hi!<br>
					<em>How are you?</em><br>
					Here is the <a href="https://www.python.org">link</a> you wanted.
				</p>
				<table style=\"width:100%\">
				"""
	htmlEnd= """\
				</table>
			</body>
		</html>
		"""

	table= "<tr>"
	for header in feedJSON['headers']:
		table+= "<th>"+header+"</th>"
	table+= "</tr>"


	for row in feedJSON['rows']:
		table+= "<tr>"
		for col in row:
			table+= "<td>" + col + "</td>"
		table+= "</tr>"

	return htmlStart+table+htmlEnd


def sendEmail(feedJSON):
	#sender and recipient
	me= "DocsTest1@docse3testtenant.onmicrosoft.com"
	you= "njn27@cornell.edu"

	#message container
	msg= MIMEMultipart('alternative')
	msg['Subject']= "Python email test"
	msg['From']= me
	msg['To']= you

	#message body 
	html= constructEmail(feedJSON)
	print "Completed writing email!"

	#Record MIME types of both parts
	part= MIMEText(html,'html')
	msg.attach(part)
	print "Attached to container!"

	#send message via local SMTP server
	mail = smtplib.SMTP('smtp.office365.com', 587)

	mail.starttls()

	mail.login(me, 'Password!!')
	mail.sendmail(me, you, msg.as_string())
	mail.quit()


if __name__ == "__main__":
	sendEmail("")
