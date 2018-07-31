#!/usr/bin/python
#coding:utf-8
#yangy114 2017-12-14

class GitlabWebhookEventUserCreate(object):
    def __init__(self, dataDict):
        self.username = dataDict["username"]
        self.userId = dataDict["user_id"]
        self.eventName = dataDict["event_name"]
        self.createdAt = dataDict["created_at"]
        self.updatedAt = dataDict["updated_at"]
        self.email = dataDict["email"]

class gitlabWebhookEventProjectDestroy(object):
    def __init__(self, dataDict):
        eventName = dataDict["event_name"]
