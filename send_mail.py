#!/usr/bin/python
 
# currently set up and tested on gmail only
 
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os, sys, base64
 
def mail(gmail_user, enc_pwd, to, subject, body, attach=None):
    msg = MIMEMultipart()
 
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
 
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)
 
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, base64.b64decode(enc_pwd))
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()
 
def main():
    if len(sys.argv) <6:
        print "Usage: send_email.py <from> <enc_pwd> <to> <subject> <body> " \
              "[<attachments>]"
        print "Note: Email is being sent in html mode, so any newlines should " \
              "be sent as <br/>"
        if len(sys.argv) > 1:
            print "\nThe following arguements were received:"
            for i in sys.argv:
                print i
    else:
        gmail_user  = sys.argv[1]
        gmail_pwd   = sys.argv[2]
        to          = sys.argv[3]
        subject     = sys.argv[4]
        body        = sys.argv[5]
        attach      = None
        if len(sys.argv) >= 7:
            attach  = sys.argv[6]
       
        mail(gmail_user, gmail_pwd, to, subject, body, attach)
 
if __name__ == '__main__':
    main()

