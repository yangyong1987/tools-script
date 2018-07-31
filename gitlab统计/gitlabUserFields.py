#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests

class GitlabUserFields(object):
    def __init__(self, userdata):
        self.id, \
        self.name, \
        self.username, \
        self.state, \
        self.avatar_url, \
        self.web_url, \
        self.created_at, \
        self.organization, \
        self.last_sign_in_at, \
        self.confirmed_at, \
        self.last_activity_on, \
        self.email, \
        self.projects_limit, \
        self.identities_provider, \
        self.identities_extern_uid, \
        self.can_create_group, \
        self.can_create_project, \
        self.two_factor_enabled, \
        self.external, \
        self.is_admin = self._GetUserInfo(userdata)
        
    def _GetUserInfo(self, data):
        try:
            id = data["id"]
        except:
            id = ""
        try:
            name = data["name"]
        except:
            name = ""
        try:
            username = data["username"]
        except:
            username = ""
        try:
            state = data["state"]
        except:
            state = ""
        try:
            avatar_url = data["avatar_url"]
        except:
            avatar_url = ""
        try:
            web_url = data["web_url"]
        except:
            web_url = ""
        try:
            created_at = data["created_at"]
        except:
            created_at = ""
        try:
            organization = data["organization"]
        except:
            organization = ""
        try:
            last_sign_in_at = data["last_sign_in_at"]
        except:
            last_sign_in_at = ""
        try:
            confirmed_at = data["confirmed_at"]
        except:
            confirmed_at = ""
        try:
            last_activity_on = data["last_activity_on"]
        except:
            last_activity_on = ""
        try:
            email = data["email"]
        except:
            email = ""
        try:
            projects_limit = data["projects_limit"]
        except:
            projects_limit = ""
        try:
            identities_provider = data["identities"][0]["provider"]
        except:
            identities_provider = ""
        try:
            identities_extern_uid = data["identities"][0]["extern_uid"]
        except:
            identities_extern_uid = ""
        try:
            can_create_group = data["can_create_group"]
        except:
            can_create_group = "" 
        try:
            can_create_project = data["can_create_project"]
        except:
            can_create_project = ""
        try:
            two_factor_enabled = data["two_factor_enabled"]
        except:
            two_factor_enabled = ""
        try:
            external = data["external"]
        except:
            external = ""
        try:
            is_admin = data["is_admin"]
        except:
            is_admin = ""

        return id, \
               name, \
               username, \
               state, \
               avatar_url, \
               web_url, \
               created_at, \
               organization, \
               last_sign_in_at, \
               confirmed_at, \
               last_activity_on, \
               email, \
               projects_limit, \
               identities_provider, \
               identities_extern_uid, \
               can_create_group, \
               can_create_project, \
               two_factor_enabled, \
               external, \
               is_admin
