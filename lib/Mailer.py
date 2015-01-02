#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Mailer:

    def __init__(self, username, passwd, fromaddr):
        self.username = username;
        self.passwd = passwd;
        self.fromaddr = fromaddr
        self.server = smtplib.SMTP('smtp.gmail.com:587')

    def send(self, toaddr, subject, body):
        msg = self.to_msg(toaddr, subject, body)
        self.server.starttls()
        self.server.login(self.username, self.passwd)
        self.server.sendmail(self.fromaddr, toaddr, msg.as_string())
        self.server.quit()

    def to_msg(self, toaddr, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        return msg
