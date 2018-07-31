#!/usr/bin/python
#coding:utf-8
#yangy114 2018-03-01

import requests

class VKGitlabApi(object):

    @staticmethod
    def PutExternalTrue(url, userid, private_token):
        urlPut = "%s/api/v4/users/%s?private_token=%s&external=True" % (url, userid, private_token)
        put = requests.put(urlPut)    
