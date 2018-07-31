#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests

class GitlabGroupFields(object):
    def __init__(self, groupdata):
        #print groupdata
        self.group_id, \
        self.group_name, \
        self.group_path, \
        self.group_description, \
        self.group_visibility, \
        self.group_lfs_enabled, \
        self.group_avatar_url, \
        self.group_web_url, \
        self.group_request_access_enabled, \
        self.group_full_name, \
        self.group_full_path, \
        self.group_parent_id, \
        self.group_projects_name = self._GetGroupsInfo(groupdata)
        
    def _GetGroupsInfo(self, data):
        try:
            group_id = data["id"]
        except:
            group_id = ""
        try:
            group_name = data["name"]
        except:
            group_name = ""
        try:
            group_path = data["path"]
        except:
            group_path = ""
        try:
            group_description = data["description"]
        except:
            group_description = ""
        try:
            group_visibility = data["visibility"]
        except:
            group_visibility = ""
        try:
            group_lfs_enabled = data["lfs_enabled"]
        except:
            group_lfs_enabled = ""
        try:
            group_avatar_url = data["avatar_url"]
        except:
            group_avatar_url = ""
        try:
            group_web_url = data["web_url"]
        except:
            group_web_url = ""
        try:
            group_request_access_enabled = data["request_access_enabled"]
        except:
            group_request_access_enabled = ""
        try:
            group_full_name = data["full_name"]
        except:
            group_full_name = ""
        try:
            group_full_path = data["full_path"]
        except:
            group_full_path = ""
        try:
            group_parent_id = data["parent_id"]
        except:
            group_parent_id = ""
        try:
            group_projects_list = data["projects"]
            group_projects_id = ""
            group_projects_name = group_projects_list[0]["name"]
            for i in group_projects_list[1:]:
                group_projects_name = group_projects_name + "," + i["name"]
        except:
            group_projects_name = ""
        
        return group_id, \
               group_name, \
               group_path, \
               group_description, \
               group_visibility, \
               group_lfs_enabled, \
               group_avatar_url, \
               group_web_url, \
               group_request_access_enabled, \
               group_full_name, \
               group_full_path, \
               group_parent_id, \
               group_projects_name
