#!/usr/bin/python
# coding:utf-8
#yangy114 2017-12-14

import json
import os
import requests
import time
import random
from jira import JIRA
from vkJiraIssueFields import VKIssueFields
from vkJiraInfo import JiraInfo
from vkJiraWebhookTpye import WebhookEvent
from vkLog import Log
from vkJiraRole import Role
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Jirasd2Jira(object):
    def __init__(self, dataDict):
        jirasd = JIRA(JiraInfo.jirasdUrl, basic_auth=(JiraInfo.jirasdUser, JiraInfo.jirasdPasswd))
        jira = JIRA(JiraInfo.jiraUrl, basic_auth=(JiraInfo.jiraUser, JiraInfo.jiraPasswd))

        issue_key = self.GetJiraKey(dataDict)
        if issue_key != "":
            issue = jirasd.issue(issue_key)
            vkissue = VKIssueFields(JiraInfo.jirasdUrl,JiraInfo.jirasdUser,JiraInfo.jirasdPasswd,issue)

        #webhookEvent = self.GetWebhookEvent(dataDict)
        #if webhookEvent == WebhookEvent.webhookEventIssueCreated:
        #    if vkissue.issueFieldsCustomfield_10300SunprojectValue == unicode("RM(资源管理系统)", "utf-8"):
        #        self.ExecuteRM(vkissue, jira)
        #elif webhookEvent == WebhookEvent.webhookEventIssueUpdated:
        #    if vkissue.issueFieldsCustomfield_10300SunprojectValue == unicode("黑猫二号", "utf-8"):
        #        self.ExecuteBlackCat2(vkissue, jira)
        #else:
        #    Log.tlog(vkissue.issueFieldsCustomfield_10300SunprojectValue)
        if vkissue.issueFieldsCustomfield_10300SunprojectValue == unicode("RM(资源管理系统)", "utf-8"):
            Log.tlog("stop update RM")
            #self.ExecuteRM(vkissue, jira)
        elif vkissue.issueFieldsCustomfield_10300SunprojectValue == unicode("黑猫二号", "utf-8"):
            self.ExecuteBlackCat2(vkissue, jira)
        else:
            Log.tlog(vkissue.issueFieldsCustomfield_10300SunprojectValue)

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

    # 更新jirasd issue单的labels
    def UpdateJirasdIssueLabels(self, issue):
        Log.tlog("begin to update the labels of jirasd.")
        issue_dict = {
            'labels': ['DONE_FLAG']
        }
        try:
            issue.update(fields=issue_dict)
        except Exception as e:
            Log.tlog(e)

    # 更新jirasd issue单的描述
    def UpdateJirasdIssueDescription(self, issue, description):
        Log.tlog("begin to update the description of jirasd.")
        issue_dict = {
            'description': description
        }
        try:
            issue.update(fields=issue_dict)
        except Exception as e:
            Log.tlog(e)

    def UpdatePriority(self, priorityID):
        if str(priorityID) == "4":
            return "3"
        else:
            return str(priorityID)
    
    def ReturnRandon(self, rlist):
        return random.choice(rlist)

    def CreateJiraIssue(self, jira, projectKey, summary, description, priorityID, labels):
        #将jirasd传过来的issue key写到environment中，以便回写jirasd 时能找到是哪个jirasd的issue。
        #print "priorityID",priorityID
        if projectKey == unicode("黑猫二号", "utf-8"):
            newProjectKey = "BLACKCAT2"
            assigneeName = Role.blackCat2CreateIssueAssigneeName
            reporterName = Role.blackCat2CreateIssueReporterName
            versionsName = "V1.0"
            componentsName = unicode("后台系统", "utf-8")
        elif projectKey == unicode("RM(资源管理系统)", "utf-8"):
            newProjectKey = "RM"
            assigneeName = self.ReturnRandon(Role.rmCreateIssueAssigneeNameL)
            reporterName = Role.rmCreateIssueReporterName
            versionsName = "v2.4.0"
            componentsName = unicode("月休", "utf-8")
        else:
            newProjectKey = "DEM"
            Log.tlog("error ...")
        issue_dict = {
            'project': {'key': newProjectKey},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Bug'},
            'labels': [labels],
            'components': [{'name': componentsName}],
            'versions': [{'name': versionsName}],
            'priority': {'id': "1" },
            'assignee': {'name': assigneeName},
            'reporter': {'name': reporterName},
            'customfield_10600': {'value': 'PROD_WYIT'}
        }
        log = "begin to craet issue in project %s" % (newProjectKey)
        Log.tlog(log)
        new_issue = jira.create_issue(fields=issue_dict)
        Log.tlog(new_issue)
        return new_issue

    # 下载附件到本地
    def DownloadJirasdAttachment(self,issueFieldsAttachmentFilenameList,issueFieldsAttachmentContentList):
        #Log.tlog("Download jirasd attachment")
        for i in range(len(issueFieldsAttachmentFilenameList)):
            re = requests.get(issueFieldsAttachmentContentList[i],auth=(JiraInfo.jirasdUser, JiraInfo.jirasdPasswd))
            with open(issueFieldsAttachmentFilenameList[i],'wb') as f:
                f.write(re.content)

    def AddJirasdIssueAttachment(self, jira, issue, issueFieldsAttachmentFilenameList):
        #Log.tlog("Add jirasd issue attachment")
        if issueFieldsAttachmentFilenameList != []:
            for i in range(len(issueFieldsAttachmentFilenameList)):
                #jira.add_attachment(issue=issue, attachment=issueFieldsAttachmentFilenameList[i])
                cmd = 'curl -D- -u %s:%s -X POST -H "X-Atlassian-Token: nocheck" -F "file=@%s" %s/rest/api/2/issue/%s/attachments' % (JiraInfo.jiraUser, JiraInfo.jiraPasswd, issueFieldsAttachmentFilenameList[i], JiraInfo.jiraUrl, str(issue))
                os.system(cmd)

    def RemoveLocalAttachment(self, issueFieldsAttachmentFilenameList):
        #Log.tlog("Remove local attachment")
        if issueFieldsAttachmentFilenameList != []:
            for i in range(len(issueFieldsAttachmentFilenameList)):
                os.remove(issueFieldsAttachmentFilenameList[i])

    def ExecuteBlackCat2(self, vkissue, jira):
        defatultProjectKey = "VSIH"
        defaultAssigneeDisplayname = unicode("JIRA问题对接", "utf-8")
        if vkissue.issueFieldsLabels != []:
            done_flag = vkissue.issueFieldsLabels[0]
        else:
            done_flag = ""
        if vkissue.issueFieldsProjectKey != defatultProjectKey or done_flag == "DONE_FLAG" or vkissue.issueFieldsStatusStatusCategoryKey == "done":
            log = "the project is %s, and StatusStatusCategoryKey is %s,maybe the labels is DONE_FLAG," % (vkissue.issueFieldsProjectKey, vkissue.issueFieldsStatusStatusCategoryKey)
            Log.tlog(log)
        else:
            if vkissue.issueFieldsAssigneeDisplayName == defaultAssigneeDisplayname:
                # 将jirasd 的issue链接添加到jira issue单的描述中，方便查找。
                jiraNewDescription = JiraInfo.jirasdUrl + "/browse/" + str(vkissue.issue) + "\n" + vkissue.issueFieldsDescription + "\n\n" + unicode("jirasd的所有评论如下:\n", "utf-8") + vkissue.issueFieldsCommentAllFormat1
                newIssue = self.CreateJiraIssue(jira, vkissue.issueFieldsCustomfield_10300SunprojectValue, vkissue.issueFieldsSummary, jiraNewDescription, self.UpdatePriority(vkissue.issueFieldsPriorityID), vkissue.issueKey)
                jirasdNewDescription = JiraInfo.jiraUrl + "/browse/" + str(newIssue) + "\n" + vkissue.issueFieldsDescription
                if vkissue.issueFieldsAttachmentFilenameList != [] and vkissue.issueFieldsAttachmentContentList != []:
                    self.DownloadJirasdAttachment(vkissue.issueFieldsAttachmentFilenameList, vkissue.issueFieldsAttachmentContentList)
                    self.AddJirasdIssueAttachment(jira, newIssue, vkissue.issueFieldsAttachmentFilenameList)
                    self.RemoveLocalAttachment(vkissue.issueFieldsAttachmentFilenameList)
                self.UpdateJirasdIssueLabels(vkissue.issue)
                self.UpdateJirasdIssueDescription(vkissue.issue, jirasdNewDescription)
            else:
                log = "Unneed to create the issue, issueFieldsAssigneeDisplayName is %s" % vkissue.issueFieldsAssigneeDisplayName
                Log.tlog(log)

    def ExecuteRM(self, vkissue, jira):
        defatultProjectKey = "VSIH"
        if vkissue.issueFieldsLabels != []:
            done_flag = vkissue.issueFieldsLabels[0]
        else:
            done_flag = ""
        if vkissue.issueFieldsProjectKey != defatultProjectKey or done_flag == "DONE_FLAG" or vkissue.issueFieldsStatusStatusCategoryKey == "done":
            log = "the project is %s, and StatusStatusCategoryKey is %s,maybe the labels is DONE_FLAG," % (vkissue.issueFieldsProjectKey, vkissue.issueFieldsStatusStatusCategoryKey)
            Log.tlog(log)
        else:
            jiraNewDescription = JiraInfo.jirasdUrl + "/browse/" + str(vkissue.issue) + "\n" + vkissue.issueFieldsDescription + "\n\n" + unicode("jirasd的所有评论如下:\n", "utf-8") + vkissue.issueFieldsCommentAllFormat1
            newIssue = self.CreateJiraIssue(jira, vkissue.issueFieldsCustomfield_10300SunprojectValue, vkissue.issueFieldsSummary, jiraNewDescription, self.UpdatePriority(vkissue.issueFieldsPriorityID), vkissue.issueKey)
            jirasdNewDescription = JiraInfo.jiraUrl + "/browse/" + str(newIssue) + "\n" + vkissue.issueFieldsDescription
            if vkissue.issueFieldsAttachmentFilenameList != [] and vkissue.issueFieldsAttachmentContentList != []:
                self.DownloadJirasdAttachment(vkissue.issueFieldsAttachmentFilenameList, vkissue.issueFieldsAttachmentContentList)
                self.AddJirasdIssueAttachment(jira, newIssue, vkissue.issueFieldsAttachmentFilenameList)
                self.RemoveLocalAttachment(vkissue.issueFieldsAttachmentFilenameList)
            self.UpdateJirasdIssueLabels(vkissue.issue)
            self.UpdateJirasdIssueDescription(vkissue.issue, jirasdNewDescription)

if __name__ == '__main__':
    dataDict = {
            "issue_event_type_name": "issue_updated",
            'issue': {'key': 'VSIH-40818'}
        }
    a = Jirasd2Jira(dataDict)
