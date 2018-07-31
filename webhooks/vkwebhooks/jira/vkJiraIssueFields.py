#!/usr/bin/python
# coding:utf-8

import requests
#from jira import JIRA

class VKIssueFields(object):
    def __init__(self, server, username, password, issue):
        self.issue = issue
        issueApi = "%s/rest/api/2/issue/%s" % (server, str(issue))
        issueDir = requests.get(issueApi, auth=(username, password))
        self.issueJson = issueDir.json()
        #print issueApi

        # === part 1 ===
        # key
        self.issueKey = self._GetIssueKey(issueDir.json())
        # project
        self.issueFieldsProjectKey = self._GetIssueFieldsProjectKey(issueDir.json())
        self.issueFieldsProjectID = self._GetIssueFieldsProjectID(issueDir.json())
        self.issueFieldsProjectName = self._GetIssueFieldsProjectName(issueDir.json())
        # issuetype
        self.issueFieldsIssuetypeID = self._GetIssueFieldsIssuetypeID(issueDir.json())
        self.issueFieldsIssuetypeName = self._GetIssueFieldsIssuetypeName(issueDir.json())
        # priority
        self.issueFieldsPriorityID = self._GetIssueFieldsPriorityID(issueDir.json())
        self.issueFieldsPriorityName = self._GetIssueFieldsPriorityName(issueDir.json())
        # assignee
        self.issueFieldsAssigneeName = self._GetIssueFieldsAssigneeName(issueDir.json())
        self.issueFieldsAssigneeKey = self._GetIssueFieldsAssigneeKey(issueDir.json())
        self.issueFieldsAssigneeEmailAddress = self._GetIssueFieldsAssigneeEmailAddress(issueDir.json())
        self.issueFieldsAssigneeDisplayName = self._GetIssueFieldsAssigneeDisplayName(issueDir.json())
        # creator
        self.issueFieldsCreatorName = self._GetIssueFieldsCreatorName(issueDir.json())
        self.issueFieldsCreatorKey = self._GetIssueFieldsCreatorKey(issueDir.json())
        self.issueFieldsCreatorEmailAddress = self._GetIssueFieldsCreatorEmailAddress(issueDir.json())
        self.issueFieldsCreatorDisplayName = self._GetIssueFieldsCreatorDisplayName(issueDir.json())
        # reporter
        self.issueFieldsReporterName = self._GetIssueFieldsReporterName(issueDir.json())
        self.issueFieldsReporterKey = self._GetIssueFieldsReporterKey(issueDir.json())
        self.issueFieldsReporterEmailAddress = self._GetIssueFieldsReporterEmailAddress(issueDir.json())
        self.issueFieldsReporterDisplayName = self._GetIssueFieldsReporterDisplayName(issueDir.json())
        # status
        self.issueFieldsStatusID = self._GetIssueFieldsStatusID(issueDir.json())
        self.issueFieldsStatusName = self._GetIssueFieldsStatusName(issueDir.json())
        self.issueFieldsStatusDescription = self._GetIssueFieldsStatusDescription(issueDir.json())
        self.issueFieldsStatusStatusCategoryID = self._GetIssueFieldsStatusStatusCategoryID(issueDir.json())
        self.issueFieldsStatusStatusCategoryKey = self._GetIssueFieldsStatusStatusCategoryKey(issueDir.json())
        self.issueFieldsStatusStatusCategoryName = self._GetIssueFieldsStatusStatusCategoryName(issueDir.json())
        # comment
        self.issueFieldsCommentTotal = self._GetIssueFieldsCommentTotal(issueDir.json())
        self.issueFieldsCommentComments = self._GetIssueFieldsCommentComments(issueDir.json())
        # resolution
        self.issueFieldsResolutionName = self._GetIssueFieldsResolutionName(issueDir.json())
        self.issueFieldsResolutionID = self._GetIssueFieldsResolutionID(issueDir.json())
        # summary, labels
        self.issueFieldsSummary = self._GetIssueFieldsSummary(issueDir.json())
        self.issueFieldsLabels = self._GetIssueFieldsLabels(issueDir.json())
        # attachment
        self.issueFieldsAttachment = self._GetIssueFieldsAttachment(issueDir.json())
        self.issueFieldsDescription = self._GetIssueFieldsDescription(issueDir.json())
        # customfield
        self.issueFieldsCustomfield_10600DiscEnvironment = self._GetIssueFieldsCustomfield_10600Value(issueDir.json())
        self.issueFieldsCustomfield_10300SunprojectValue = self._GetIssueFieldsCustomfield_10300Value(issueDir.json())
        #self.issueFieldsCustomfield_10701BelongsValue = self._GetIssueFieldsCustomfield_10701Value(issueDir.json())

        # === part 2 ===
        self.issueFieldsAttachmentFilenameList, self.issueFieldsAttachmentContentList = self._GetIssueFieldsAttachmentFilenameContentList(self.issueFieldsAttachment)
        self.issueFieldsCommentAllFormat1 = self._GetIssueFieldsCommentAllFormat1(self.issueFieldsCommentComments)

    # get key
    def _GetIssueKey(self, issueDir):
        try:
            issueKey = issueDir["key"]
        except:
            issueKey = ""
        return issueKey

    # get project
    def _GetIssueFieldsProjectKey(self, issueJson):
        try:
            issueFieldsProjectKey = issueJson["fields"]["project"]["key"]
        except:
            issueFieldsProjectKey = ""
        return issueFieldsProjectKey

    def _GetIssueFieldsProjectID(self, issueJson):
        try:
            issueFieldsProjectID = issueJson["fields"]["project"]["id"]
        except:
            issueFieldsProjectID = ""
        return issueFieldsProjectID

    def _GetIssueFieldsProjectName(self, issueJson):
        try:
            issueFieldsProjectName = issueJson["fields"]["project"]["name"]
        except:
            issueFieldsProjectName = ""
        return issueFieldsProjectName

    # get issuetype
    def _GetIssueFieldsIssuetypeID(self, issueJson):
        try:
            issueFieldsIssuetypeID = issueJson["fields"]["issuetype"]["id"]
        except:
            issueFieldsIssuetypeID = ""
        return issueFieldsIssuetypeID

    def _GetIssueFieldsIssuetypeName(self, issueJson):
        try:
            issueFieldsIssuetypeName = issueJson["fields"]["issuetype"]["name"]
        except:
            issueFieldsIssuetypeName = ""
        return issueFieldsIssuetypeName

    # get priority
    def _GetIssueFieldsPriorityID(self, issueJson):
        try:
            issueFieldsPriorityID = issueJson["fields"]["priority"]["id"]
        except:
            issueFieldsPriorityID = ""
        return issueFieldsPriorityID

    def _GetIssueFieldsPriorityName(self, issueJson):
        try:
            issueFieldsPriorityName = issueJson["fields"]["priority"]["name"]
        except:
            issueFieldsPriorityName = ""
        return issueFieldsPriorityName

    # get assignee
    def _GetIssueFieldsAssigneeName(self, issueJson):
        try:
            issueFieldsAssigneeName = issueJson["fields"]["assignee"]["name"]
        except:
            issueFieldsAssigneeName = ""
        return issueFieldsAssigneeName

    def _GetIssueFieldsAssigneeKey(self, issueJson):
        try:
            issueFieldsAssigneeKey = issueJson["fields"]["assignee"]["key"]
        except:
            issueFieldsAssigneeKey = ""
        return issueFieldsAssigneeKey

    def _GetIssueFieldsAssigneeEmailAddress(self, issueJson):
        try:
            issueFieldsAssigneeEmailAddress = issueJson["fields"]["assignee"]["emailAddress"]
        except:
            issueFieldsAssigneeEmailAddress = ""
        return issueFieldsAssigneeEmailAddress

    def _GetIssueFieldsAssigneeDisplayName(self, issueJson):
        try:
            issueFieldsAssigneeDisplayName = issueJson["fields"]["assignee"]["displayName"]
        except:
            issueFieldsAssigneeDisplayName = ""
        return issueFieldsAssigneeDisplayName

    # get creator
    def _GetIssueFieldsCreatorName(self, issueJson):
        try:
            issueFieldsCreatorName = issueJson["fields"]["creator"]["name"]
        except:
            issueFieldsCreatorName = ""
        return issueFieldsCreatorName

    def _GetIssueFieldsCreatorKey(self, issueJson):
        try:
            issueFieldsCreatorKey = issueJson["fields"]["creator"]["key"]
        except:
            issueFieldsCreatorKey = ""
        return issueFieldsCreatorKey

    def _GetIssueFieldsCreatorEmailAddress(self, issueJson):
        try:
            issueFieldsCreatorEmailAddress = issueJson["fields"]["creator"]["emailAddress"]
        except:
            issueFieldsCreatorEmailAddress = ""
        return issueFieldsCreatorEmailAddress

    def _GetIssueFieldsCreatorDisplayName(self, issueJson):
        try:
            issueFieldsCreatorDisplayName = issueJson["fields"]["creator"]["displayName"]
        except:
            issueFieldsCreatorDisplayName = ""
        return issueFieldsCreatorDisplayName

    #get reporter
    def _GetIssueFieldsReporterName(self, issueJson):
        try:
            issueFieldsReporterName = issueJson["fields"]["reporter"]["name"]
        except:
            issueFieldsReporterName = ""
        return issueFieldsReporterName

    def _GetIssueFieldsReporterKey(self, issueJson):
        try:
            issueFieldsReporterKey = issueJson["fields"]["reporter"]["key"]
        except:
            issueFieldsReporterKey = ""
        return issueFieldsReporterKey

    def _GetIssueFieldsReporterEmailAddress(self, issueJson):
        try:
            issueFieldsReporterEmailAddress = issueJson["fields"]["reporter"]["emailAddress"]
        except:
            issueFieldsReporterEmailAddress = ""
        return issueFieldsReporterEmailAddress

    def _GetIssueFieldsReporterDisplayName(self, issueJson):
        try:
            issueFieldsReporterDisplayName = issueJson["fields"]["reporter"]["displayName"]
        except:
            issueFieldsReporterDisplayName = ""
        return issueFieldsReporterDisplayName

    # status
    def _GetIssueFieldsStatusID(self, issueJson):
        try:
            issueFieldsStatusID = issueJson["fields"]["status"]["id"]
        except:
            issueFieldsStatusID = ""
        return issueFieldsStatusID

    def _GetIssueFieldsStatusName(self, issueJson):
        try:
            issueFieldsStatusName = issueJson["fields"]["status"]["name"]
        except:
            issueFieldsStatusName = ""
        return issueFieldsStatusName

    def _GetIssueFieldsStatusDescription(self, issueJson):
        try:
            issueFieldsStatusDescription = issueJson["fields"]["status"]["description"]
        except:
            issueFieldsStatusDescription = ""
        return issueFieldsStatusDescription

    def _GetIssueFieldsStatusStatusCategoryID(self, issueJson):
        try:
            issueFieldsStatusStatusCategoryID = issueJson["fields"]["status"]["statusCategory"]["id"]
        except:
            issueFieldsStatusStatusCategoryID = ""
        return issueFieldsStatusStatusCategoryID

    def _GetIssueFieldsStatusStatusCategoryKey(self, issueJson):
        try:
            issueFieldsStatusStatusCategoryKey = issueJson["fields"]["status"]["statusCategory"]["key"]
        except:
            issueFieldsStatusStatusCategoryKey = ""
        return issueFieldsStatusStatusCategoryKey

    def _GetIssueFieldsStatusStatusCategoryName(self, issueJson):
        try:
            issueFieldsStatusStatusCategoryName = issueJson["fields"]["status"]["statusCategory"]["name"]
        except:
            issueFieldsStatusStatusCategoryName = ""
        return issueFieldsStatusStatusCategoryName

    # comment
    def _GetIssueFieldsCommentTotal(self, issueJson):
        try:
            issueFieldsCommentTotal = issueJson["fields"]["comment"]["total"]
        except:
            issueFieldsCommentTotal = ""
        return issueFieldsCommentTotal

    def _GetIssueFieldsCommentComments(self, issueJson):
        try:
            issueFieldsCommentComments = issueJson["fields"]["comment"]["comments"]
        except:
            issueFieldsCommentComments = []
        return issueFieldsCommentComments

    # attachment
    def _GetIssueFieldsAttachment(self, issueJson):
        try:
            issueFieldsAttachment = issueJson["fields"]["attachment"]
        except:
            issueFieldsAttachment = []
        return issueFieldsAttachment

    # summary
    def _GetIssueFieldsSummary(self, issueJson):
        try:
            issueFieldsSummary = issueJson["fields"]["summary"]
        except:
            issueFieldsSummary = ""
        return issueFieldsSummary

    # resolution
    def _GetIssueFieldsResolutionName(self, issueJson):
        try:
            issueFieldsResolutionName = issueJson["fields"]["resolution"]["name"]
        except:
            issueFieldsResolutionName = ""
        return issueFieldsResolutionName

    def _GetIssueFieldsResolutionID(self, issueJson):
        try:
            issueFieldsResolutionID = issueJson["fields"]["resolution"]["id"]
        except:
            issueFieldsResolutionID = ""
        return issueFieldsResolutionID

    # labels
    def _GetIssueFieldsLabels(self, issueJson):
        try:
            issueFieldsLabels = issueJson["fields"]["labels"]
        except:
            issueFieldsLabels = []
        return issueFieldsLabels

    # description
    def _GetIssueFieldsDescription(self, issueJson):
        try:
            issueFieldsDescription = issueJson["fields"]["description"]
        except:
            issueFieldsDescription = ""
        return issueFieldsDescription

    # customfield
    def _GetIssueFieldsCustomfield_10600Value(self, issueJson):
        try:
            discEnvironment = issueJson["fields"]["customfield_10600"]["value"]
        except:
            discEnvironment = ""
        return discEnvironment

    def _GetIssueFieldsCustomfield_10300Value(self, issueJson):
        try:
            sunprojectValue = issueJson["fields"]["customfield_10300"]["value"]
        except:
            sunprojectValue = ""
        return sunprojectValue

    #def _GetIssueFieldsCustomfield_10701Value(self, issueJson):
    #    try:
    #        belongsValue = issueJson["fields"]["customfield_10701"]["value"]
    #    except:
    #        belongsValue = ""
    #    return belongsValue

    def _GetIssueFieldsAttachmentFilenameContentList(self, issueFieldsAttachment):
        issueFieldsAttachmentFilenameList = []
        issueFieldsAttachmentContentList = []
        if issueFieldsAttachment != []:
            for i in range(len(issueFieldsAttachment)):
                attachmentFilename = issueFieldsAttachment[i]["filename"]
                attachmentContent = issueFieldsAttachment[i]["content"]
                issueFieldsAttachmentFilenameList.append(attachmentFilename)
                issueFieldsAttachmentContentList.append(attachmentContent)
        return issueFieldsAttachmentFilenameList, issueFieldsAttachmentContentList

    def _GetIssueFieldsCommentAllFormat1(self, issueFieldsCommentComments):
        issueFieldsCommentAllFormat1 = ""
        if issueFieldsCommentComments != []:
            for i in range(len(issueFieldsCommentComments)):
                displayName = issueFieldsCommentComments[i]["updateAuthor"]["displayName"]
                emailAddress = issueFieldsCommentComments[i]["updateAuthor"]["emailAddress"]
                comment = issueFieldsCommentComments[i]["body"]
                j = displayName + ": " + emailAddress + "\n" + comment + "\n\n"
                issueFieldsCommentAllFormat1 = issueFieldsCommentAllFormat1 + j
        return issueFieldsCommentAllFormat1


if __name__ == "__main__":
    l = VKIssueFields("http://10.0.57.72:8080", "vk_test", "vk_test","VKHEL-118")
    #l = VKIssueFields("http://jira.vankeservice.com:8080", "adminjira", "vanke123", "DEM-242")
    # key
    print l.issueKey
    # project
    print "\n" + "== project"
    print l.issueFieldsProjectKey
    print l.issueFieldsProjectID
    print l.issueFieldsProjectName
    # issuetype
    print "\n" + "== issuetype"
    print l.issueFieldsIssuetypeID
    print l.issueFieldsIssuetypeName
    # priority
    print "\n" + "== priority"
    print l.issueFieldsPriorityID
    print l.issueFieldsPriorityName
    # assignee
    print "\n" + "== assignee"
    print l.issueFieldsAssigneeName
    print l.issueFieldsAssigneeKey
    print l.issueFieldsAssigneeEmailAddress
    print l.issueFieldsAssigneeDisplayName
    # creator
    print "\n" + "== creator"
    print l.issueFieldsCreatorName
    print l.issueFieldsCreatorKey
    print l.issueFieldsCreatorEmailAddress
    print l.issueFieldsCreatorDisplayName
    # reporter
    print "\n" + "== reporter"
    print l.issueFieldsReporterName
    print l.issueFieldsReporterKey
    print l.issueFieldsReporterEmailAddress
    print l.issueFieldsReporterDisplayName
    # status
    print "\n" + "== status"
    print l.issueFieldsStatusID
    print l.issueFieldsStatusName
    print l.issueFieldsStatusDescription
    print l.issueFieldsStatusStatusCategoryID
    print l.issueFieldsStatusStatusCategoryKey
    print l.issueFieldsStatusStatusCategoryName
    # comment
    print "\n" + "== comment"
    print l.issueFieldsCommentTotal
    print l.issueFieldsCommentComments
    # attachment, summary, resolution, labels
    print "\n" + "== attachment, summary, resolution, labels"
    print l.issueFieldsAttachment
    print l.issueFieldsSummary
    print l.issueFieldsResolution
    print l.issueFieldsLabels
    print l.issueFieldsDescription
    # other
    print l.issueFieldsAttachmentFilenameList
    print l.issueFieldsAttachmentContentList
    print l.issueFieldsCommentAllFormat1

