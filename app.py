#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
from datetime import datetime, date, timedelta

from lib import json_io
from lib.FB import FB
from lib.Mailer import Mailer

def stream_summary(stream, post_number=10):
    stream_msg = ""
    count = 0
    try:
        for post in stream[u'data']:
            if is_one_day(post[u'updated_time']):
                stream_msg += post['from']['name'].encode('utf-8') + ': \n'
                stream_msg += status(post)
                if post['type'] == 'photo':
                    stream_msg += 'picture' + photo(post)
                elif post['type'] == 'link':
                    stream_msg += 'link:' + link(post)
                elif post['type'] == 'video':
                    stream_msg += 'video:' + video(post)

                stream_msg += '------------------\n'
            count += 1
            if count > post_number:
                break
    except KeyError:
        print 'KeyError.'
        exit(-1)

    return stream_msg

def status(post):
    status = ""
    if 'message' in post:
       status += post['message'].encode('utf-8') + '\n'
    if 'story' in post:
       status += post['story'].encode('utf-8') + '\n'
    return status

def photo(post):
    return post['picture'].encode('utf-8') + '\n'

def video(post):
    return post['link'].encode('utf-8') + '\n'

def link(post):
    return post['link'].encode('utf-8') + '\n'

def notification_summary(notifications):
    noti_msg = ""
    try:
        for msg in notifications[u'data']:
            if is_one_day(msg[u'updated_time']):
                noti_msg += msg['title'].encode('utf-8') + ': \n'
                noti_msg += msg['link'].encode('utf-8') + '\n'
                noti_msg += '------------------\n'
    except KeyError:
        print 'KeyError.'
        exit(-1)
    return noti_msg

def mailbox_summary(inbox):
    inbox_msg = ""
    try:
        for chat_box in inbox[u'data']:
            if is_one_day(chat_box[u'updated_time']):
                msgs = chat_box['comments']
                for msg in msgs['data']:
                    inbox_msg += msg['from']['name'].encode('utf-8') + ': \n'
                    inbox_msg += msg['message'].encode('utf-8') + '\n'
                    inbox_msg += '------------------\n'
    except KeyError:
        print 'KeyError.'
        exit(-1)
    return inbox_msg

def is_one_day(updated_time):
    yesterday = datetime.today() - timedelta(days=1)  
    post_date = datetime.strptime(updated_time[:19], '%Y-%m-%dT%H:%M:%S')
    return post_date >= yesterday

if __name__=='__main__':

    user = json_io.read_json('user.json')
    fb_config = user['Facebook']
    mail_config = user['Mailer']

    fb = FB(fb_config[u'oauth_access_token'])
    mailer = Mailer(mail_config['username'], mail_config['passwd'], mail_config['fromaddr'])
    
    stream = fb.get_stream()
    notifications = fb.get_notification()
    inbox = fb.get_inbox()

    stream_msg = stream_summary(stream)
    notifications_msg = notification_summary(notifications)
    inbox_msg = mailbox_summary(inbox)
    
    fb_summary = 'News: \n %s \n Notifications \n %s \n Inbox: \n %s \n' \
                                    % (stream_msg, notifications_msg, inbox_msg)

    mailer.send(mail_config[u'toaddr'], mail_config[u'subject'] + str(date.today()), fb_summary)
