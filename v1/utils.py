
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils.html import strip_tags

def send_email(subject, body, sender, recipients, password,text_body=None):
   msg = MIMEMultipart('alternative')
   msg['Subject'] = subject
   msg['From'] = sender
   msg['To'] = ', '.join(recipients)

   if text_body is None:
      text_body = strip_tags(body)

   msg.attach(MIMEText(text_body, 'plain'))
   msg.attach(MIMEText(body, 'html'))
      
   with smtplib.SMTP_SSL('smtp.zoho.in', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
   print("Mail sent Successfully")
