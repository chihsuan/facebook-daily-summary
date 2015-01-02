#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import facebook
import requests

class FB:

    def __init__(self, oauth_access_token):
        self.graph = facebook.GraphAPI(oauth_access_token)

    def get_stream(self):
        return self.graph.get_connections("me", "home")

    def get_notification(self):
        return self.graph.get_connections("me", "notifications")

    def get_inbox(self):
        return self.graph.get_connections("me", "inbox")

    def get_profile(self):
        return self.graph.get_object("me")

    def get_posts(self):
        return graph.get_connections(profile['id'], 'posts')


