
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils.html import strip_tags

def send_email(subject, body, from_email,login_email, recipients, password,text_body=None):
   msg = MIMEMultipart('alternative')
   msg['Subject'] = subject
   msg['From'] = from_email
   msg['To'] = ', '.join(recipients)

   if text_body is None:
      text_body = strip_tags(body)

   msg.attach(MIMEText(text_body, 'plain'))
   msg.attach(MIMEText(body, 'html'))
      
   with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
       smtp_server.starttls()
       smtp_server.login(login_email, password)
       smtp_server.sendmail(from_email, recipients, msg.as_string())
   print("Mail sent Successfully")
