from decouple import config

import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from apps.operations.models import NotificationTemplate

mail_content = NotificationTemplate.objects.filter[0]

def sendEmail(full_name, email_id, phone_number):
    SENDER = config.get('SENDER')
    SENDERNAME = config.get('SENDERNAME')
    RECIPIENT  = email_id
    USERNAME_SMTP = config.get('USERNAME_STTP')
    PASSWORD_SMTP = config.get('PASSWORD_STTP')
    HOST = config.get('HOST')
    PORT = config.get('PORT')
    SUBJECT = mail_content.subject
    BODY_TEXT = mail_content.content
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    
    body = MIMEText(BODY_TEXT, 'plain')
    
    msg.attach(body)
    
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()