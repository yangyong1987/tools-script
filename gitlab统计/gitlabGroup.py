#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests

from gitlabGroupFields import GitlabGroupFields
from gitlabUserFields import GitlabUserFields

class GroupsData(object):
    def __init__(self, url, private_token):
        self.url = url
        self.private_token = private_token
        #excel的表格名称
        self.sheet = "groups"
        #excel首行标题
        self.head = ["id", \
                     "name", \
                     "description", \
                     "visibility", \
                     "web_url", \
                     "request_access_enabled", \
                     "full_path", \
                     "parent_id", \
                     "projects", \
                     "members"]
        #获取数据
        self.dataList = self._get_datalist()
    
    def _get_datalist(self):
        flag = True
        m = 0
        #每页50个数据
        perPage = 50
        #页码
        page = 0
        groups_data_list = []
        groups_id_list = []
        while flag:
            page = page + 1
            groups_api_url = "%s/api/v4/groups?private_token=%s&per_page=%s&page=%s" % (self.url, self.private_token, perPage, str(page))
            re = requests.get(groups_api_url)
            data = re.json()
            if data == []:
                flag = False
            else:
                for i in range(len(data)):
                    gs = GitlabGroupFields(data[i])
                    groups_id_list.append(gs.group_id)
        for i in groups_id_list:
            m = m + 1
            group_user = ""
            group_api_url = "%s/api/v4/groups/%s?private_token=%s&per_page=%s&page=%s" % (self.url, i, self.private_token, perPage, str(m))
            re_group = requests.get(group_api_url)
            group_data = re_group.json()
            g = GitlabGroupFields(group_data)
            group_members_aip_url = "%s/api/v4/groups/%s/members?private_token=%s" % (self.url, i, self.private_token)
            re_group_members = requests.get(group_members_aip_url)
            group_members_data = re_group_members.json()
            for j in group_members_data:
                user = GitlabUserFields(j)
                group_user = group_user + user.name + user.username + ","
            groups_data_list.append([g.group_id, \
                             g.group_name, \
                             g.group_description, \
                             g.group_visibility, \
                             g.group_web_url, \
                             g.group_request_access_enabled, \
                             g.group_full_path, \
                             g.group_parent_id, \
                             g.group_projects_name, \
                             group_user])

        return groups_data_list
