#!/usr/bin/python
#coding:utf-8
#yangy114 2018-03-01

import requests
from vkGitlabWebhookTpye import GitlabWebhookEvent
from vkEventInfo import GitlabWebhookEventUserCreate
from vkGitlabApi import VKGitlabApi
from vkGitlabInfo import GitlabInfo

class vkgitlab(object):
    def __init__(self, dataDict):
        eventName = dataDict["event_name"]

        #创建用户事件
        if eventName == GitlabWebhookEvent.gitlabWebhookEventUserCreate:
            e = GitlabWebhookEventUserCreate(dataDict)
            print e.username
            if e.username.startswith("v-"):
                print "Put %s External" % (e.username)
                VKGitlabApi.PutExternalTrue(GitlabInfo.gitlabUrl, e.userId, GitlabInfo.privateToken)

        #创建项目事件
        if eventName == GitlabWebhookEvent.gitlabWebhookEventProjectCreate:
            pass

        #push代码事件
        if eventName == GitlabWebhookEvent.gitlabWebhookEventPush:
            pass

if __name__ == '__main__':
    dataDict = {'username': 'v-test3',
            'user_id': 104,
            'name': 'test3',
            'event_name': 'user_create',
            'created_at': '2018-02-28T19:22:56+08:00',
            'updated_at': '2018-02-28T19:22:56+08:00',
            'email': 'test3@qq.com'}
    dataDict2 = {'username': 'v-test2',
            'user_id': 165,
            'name': 'test2',
            'event_name': 'user_create',
            'created_at': '2018-02-28T19:22:56+08:00',
            'updated_at': '2018-02-28T19:22:56+08:00',
            'email': 'test2@vanke.com'}
    a = vkgitlab(dataDict2)