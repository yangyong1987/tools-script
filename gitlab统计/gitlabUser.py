#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests

from gitlabUserFields import GitlabUserFields

class UsersData(object):
    def __init__(self, url, private_token):
        self.url = url
        self.private_token = private_token
        #excel的表格名称
        self.sheet = "users"
        #excel首行标题
        self.head = ["id", \
                     "name", \
                     "username", \
                     "state", \
                     "web_url", \
                     "created_at", \
                     "last_sign_in_at", \
                     "confirmed_at", \
                     "last_activity_on", \
                     "email", \
                     "projects_limit", \
                     "identities_provider", \
                     "identities_extern_uid", \
                     "can_create_group", \
                     "can_create_project", \
                     "two_factor_enabled", \
                     "external", \
                     "is_admin"]
        self.dataList = self._get_datalist()
    
    def _get_datalist(self):
        flag = True
        m = 0
        #每页50个数据
        perPage = 50
        #页码
        page = 0
        dataList = []
        users_id_list = []
        while flag:
            page = page + 1
            users_api_url = "%s/api/v4/users?private_token=%s&per_page=%s&page=%s" % (self.url, self.private_token, perPage, str(page))
            re = requests.get(users_api_url)
            data = re.json()
            if data == []:
                flag = False
            else:
                for i in range(len(data)):
                    users = GitlabUserFields(data[i])
                    users_id_list.append(users.id)
        for i in users_id_list:
            m = m + 1
            user_api_url = "%s/api/v4/users/%s?private_token=%s" % (self.url, i, self.private_token)
            re_user = requests.get(user_api_url)
            user_data = re_user.json()
            user = GitlabUserFields(user_data)
            dataList.append([user.id, \
                             user.name, \
                             user.username, \
                             user.state, \
                             user.web_url, \
                             user.created_at, \
                             user.last_sign_in_at, \
                             user.confirmed_at, \
                             user.last_activity_on, \
                             user.email, \
                             user.projects_limit, \
                             user.identities_provider, \
                             user.identities_extern_uid, \
                             user.can_create_group, \
                             user.can_create_project, \
                             user.two_factor_enabled, \
                             user.external, \
                             user.is_admin])
        return dataList
