#!/usr/bin/python
# -*- coding: utf-8 -*-
#yangy114 2017-12-14

import json
import os
import requests
import time
from jira import JIRA
from vkJiraIssueFields import VKIssueFields
from vkJiraInfo import JiraInfo
from vkJiraWebhookTpye import WebhookEvent
from vkLog import Log
from vkJiraRole import Role

# 该类是jira数据自动到jirasd
class Jira2Jirasd(object):
    def __init__(self, dataDict):
        jirasd = JIRA(JiraInfo.jirasdUrl, basic_auth=(JiraInfo.jirasdUser, JiraInfo.jirasdPasswd))
        jira = JIRA(JiraInfo.jiraUrl, basic_auth=(JiraInfo.jiraUser, JiraInfo.jiraPasswd))

        webhookEvent = self.GetWebhookEvent(dataDict)
        if webhookEvent == WebhookEvent.webhookEventComment:
            print "comment"
        elif webhookEvent == WebhookEvent.webhookEventIssueUpdated:
            issue_key = self.GetJiraKey(dataDict)
            if issue_key != "":
                issue = jira.issue(issue_key)
                vkissue = VKIssueFields(JiraInfo.jiraUrl, JiraInfo.jiraUser, JiraInfo.jiraPasswd, issue)
                self.Execute(vkissue, jirasd)
        else:
            print "null"

    def GetJiraKey(self,dataDict):
        try:
            jiraKey = dataDict["issue"]["key"]
        except:
            jiraKey = ""
        return jiraKey

    def GetWebhookEvent(self,dataDict):
        try:
            webhookEvent = dataDict["webhookEvent"]
        except:
            webhookEvent = ""
        return webhookEvent

    # 关闭jirasd上issue的函数
    # 同时将jira上的评论添加到jirasd上
    def CloseJirasdIssue(self, jirasd, issueKey, comments):
        issue = jirasd.issue(issueKey)
        if comments == "":
            comments = "no comments,auto close!"
        jirasd.add_comment(issue, comments)
        log = "close the issue %s." % issueKey
        Log.tlog(log)
        # transitions = jirasd.transitions(issue)
        # for t in transitions:
        #    print [(t['id'], t['name'])]
        jirasd.transition_issue(issue, '111')

    # jirasd上添加评论的函数
    # 将猫头鹰项目在jira上的进度以评论的方式反馈到jirasd上
    def UpdateJirasdComments(self, jirasd, issueKey, comments):
        issue = jirasd.issue(issueKey)
        vkissue = VKIssueFields(JiraInfo.jirasdUrl, JiraInfo.jirasdUser, JiraInfo.jirasdPasswd, issue)
        if comments in vkissue.issueFieldsCommentAllFormat1:
            Log.tlog("unneed update comments")
        else:
            jirasd.add_comment(issue,comments)

    # 添加DONE_FLAG到jirasd label的函数
    # 作用是要区别已经处理过的issue
    def UpdateJiraIssueLabels(self, issue, issueFieldsLabels):
        Log.tlog("begin to update the labels of jira.")
        issueFieldsLabels.append("DONE_FLAG")
        issue_dict = {
            'labels': issueFieldsLabels
        }
        try:
            issue.update(fields=issue_dict)
            Log.tlog("update over.")
        except Exception as e:
            Log.tlog(e)

    # 黑猫2号的执行逻辑
    def ExeBlackCat2(self, vkissue, jirasd):
        defaultDiscEnvironment = "PROD_WYIT"
        defaultIssueStatusStatusCategoryName = "Done"
        defaultResolutionName = ""
        defaultDoneFlag = "DONE_FLAG"
        if vkissue.issueFieldsLabels == []:
            done_flag = ""
        else:
            done_flag = vkissue.issueFieldsLabels[0]

        # 执行会写jirasd的判断条件
        if done_flag != defaultDoneFlag:
            # 判断DiscEnvironment等于PROD_WYIT才往下判断
            if vkissue.issueFieldsCustomfield_10600DiscEnvironment == defaultDiscEnvironment:
                # Resolution Name不为空则关闭jirasd issue
                if vkissue.issueFieldsResolutionName != defaultResolutionName:
                    Log.tlog("resolution is not none,so close issue.")
                    self.CloseJirasdIssue(jirasd, vkissue.issueFieldsLabels[0], vkissue.issueFieldsCommentAllFormat1)
                    self.UpdateJiraIssueLabels(vkissue.issue, vkissue.issueFieldsLabels)
                else:
                    # 状态是完成则关闭jirasd issue
                    if vkissue.issueFieldsStatusStatusCategoryName == defaultIssueStatusStatusCategoryName:
                        Log.tlog("the issue_status is done,so close issue.")
                        self.CloseJirasdIssue(jirasd, vkissue.issueFieldsLabels[0], vkissue.issueFieldsCommentAllFormat1)
                        self.UpdateJiraIssueLabels(vkissue.issue, vkissue.issueFieldsLabels)
                    else:
                        #经办人不在测试团队则关闭jirasd issue
                        if vkissue.issueFieldsAssigneeEmailAddress not in Role.blackCat2TestTeamEmailL:
                            Log.tlog("the assignee is not in the test team,so close issue.")
                            self.CloseJirasdIssue(jirasd, vkissue.issueFieldsLabels[0], vkissue.issueFieldsCommentAllFormat1)
                            self.UpdateJiraIssueLabels(vkissue.issue, vkissue.issueFieldsLabels)
                        else:
                            Log.tlog("unneed update the issue status !")
            else:
                log = "environment != %s" % (defaultDiscEnvironment)
                Log.tlog(log)
        else:
            Log.tlog("Unneed to deal with the issue, maybe it had been updated ")

    #猫头鹰的执行逻辑
    def ExeRM(self, vkissue, jirasd):
        defaultDiscEnvironment = "PROD_WYIT"
        defaultResolution = unicode("完成", "utf-8")
        defaultBelongsProduct = unicode("产品", "utf-8")
        defaultBelongsOperate = unicode("运营", "utf-8")
        defaultIssueStatus = "Done"
        comment1 = unicode("[接口人] 正在分析处理。", "utf-8")
        comment2 = unicode("经分析是个bug，[研发]正在分析处理。", "utf-8")
        comment3 = unicode("经分析是个线上问题，[产品]同事正在分析处理。", "utf-8")
        comment4 = unicode("经分析是个线上问题，[运营]同事正在分析处理。", "utf-8")
        defaultDoneFlag = "DONE_FLAG"
        defaultIssueBugName = "Bug"
        defaultIssueProdName = "Prod"
        defaultIssueOperName = "Oper"
        defaultAssigneeEmailAddressL = Role.rmCreateIssueAssigneeEmailL
        if vkissue.issueFieldsLabels == []:
            done_flag = ""
        else:
            done_flag = vkissue.issueFieldsLabels[0]
        if vkissue.issueFieldsCustomfield_10600DiscEnvironment == defaultDiscEnvironment:
            if done_flag == defaultDoneFlag:
                Log.tlog("done_flag is DONE_FLAG")
            elif vkissue.issueFieldsResolutionName == defaultResolution or vkissue.issueFieldsStatusName == defaultIssueStatus:
                Log.tlog("resolution is done,so close issue.")
                self.CloseJirasdIssue(jirasd, vkissue.issueFieldsLabels[0], vkissue.issueFieldsCommentAllFormat1)
                self.UpdateJiraIssueLabels(vkissue.issue, vkissue.issueFieldsLabels)
                self.UpdateJirasdComments(jirasd, vkissue.issueFieldsLabels[0], comment1)
            else:
                print vkissue.issueFieldsAssigneeEmailAddress
                if vkissue.issueFieldsAssigneeEmailAddress not in defaultAssigneeEmailAddressL and vkissue.issueFieldsIssuetypeName == defaultIssueBugName:#判断处理人是否已经不是测试团队
                    Log.tlog(comment2)
                    self.UpdateJirasdComments(jirasd, vkissue.issueFieldsLabels[0], comment2)
                elif vkissue.issueFieldsIssuetypeName == defaultIssueProdName:
                    Log.tlog(comment3)
                    self.UpdateJirasdComments(jirasd, vkissue.issueFieldsLabels[0], comment3)
                elif vkissue.issueFieldsIssuetypeName == defaultIssueOperName:
                    Log.tlog(comment4)
                    self.UpdateJirasdComments(jirasd, vkissue.issueFieldsLabels[0], comment4)
                else:
                    Log.tlog(comment1)
                    self.UpdateJirasdComments(jirasd, vkissue.issueFieldsLabels[0], comment1)
        else:
            log = "environment != %s" % (defaultDiscEnvironment)
            Log.tlog(log)

    def Execute(self, vkissue, jirasd):
        blackCat2ProjectKey = "BLACKCAT2"
        rmProjectKey = "RM"
        dem = "DEM"
        if vkissue.issueFieldsProjectKey == blackCat2ProjectKey:
            self.ExeBlackCat2(vkissue, jirasd)
        elif vkissue.issueFieldsProjectKey == rmProjectKey:
            Log.tlog("stop update RM")
            #self.ExeRM(vkissue, jirasd)
        else:
            log = "vkissue.issueFieldsProjectKey is %s" % (vkissue.issueFieldsProjectKey)
            Log.tlog(log)
            print vkissue.issueJson

if __name__ == '__main__':
    dataDict = {
            "issue_event_type_name": "issue_updated",
            'issue': {'key': 'DEM-263'},
            'webhookEvent': 'jira:issue_updated'
        }
    a = Jira2Jirasd(dataDict)
