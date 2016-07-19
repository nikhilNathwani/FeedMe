import smtplib 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def constructEmail(feedJSON):
	htmlStart= """\
		<html>
			<head>
				<style type="text/css">
					table {
					  border-collapse: collapse;
					  font-family: Segoe UI;
					}
					td, th {
					  border: 1px solid #999;
					  padding: 0.5rem;
					  text-align: left;
					}
					thead {
						background-color: red;
					}
					.row0 {
						background-color: blue;
					}
					.row1 {
						background-color: yellow;
					}
				</style>
			</head>
			<body>
				<p style=\"color=red\">Hi!<br>
					<em>How are you?</em><br>
					Here is the <a href="https://www.python.org">link</a> you wanted.
				</p>
				<table>
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

	parity= 0
	for row in feedJSON['rows']:
		table+= "<tr class=\"row\"" + str(parity) +">"
		for col in row:
			table+= "<td>" + col + "</td>"
		table+= "</tr>"
		parity= 0 if parity==1 else 0 

	return htmlStart+table+htmlEnd


def sendEmail(feedJSON):
	#sender and recipient
	me= "DocsTest1@docse3testtenant.onmicrosoft.com"
	you= "nikhilna@microsoft.com"

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
