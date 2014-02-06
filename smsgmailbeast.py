import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

def sendMail(recipient, subject, text):
  gmailUser = 'FareBeast@gmail.com'
  gmailPassword = '************'


  msg = MIMEMultipart()
  msg['From'] = "FareBeast" #gmailUser
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))

#  for attachmentFilePath in attachmentFilePaths:
#    msg.attach(getAttachment(attachmentFilePath))

 #Open the files in binary mode.  Let the MIMEImage class automatically
 # guess the specific image type.
  #fp = open(attachment, 'rb')
  #img = MIMEImage(fp.read())
  #fp.close()
  #msg.attach(img)

  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, recipient, msg.as_string())
  mailServer.close()

  print('Sent email to %s' % recipient)

  
