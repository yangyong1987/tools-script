#!/usr/bin/python
#coding:utf-8
#yangy114 2017-12-14

class GitlabWebhookEvent(object):
    gitlabWebhookEventProjectCreate = "project_create"
    gitlabWebhookEventProjectDestroy = "project_destroy"
    gitlabWebhookEventProjectRename = "project_rename"
    gitlabWebhookEventProjectTransfer = "project_transfer"
    gitlabWebhookEventProjectUpdate = "project_update"
    gitlabWebhookEventUserAddToTeam = "user_add_to_team"
    gitlabWebhookEventUserRemoveFromTeam = "user_remove_from_team"
    gitlabWebhookEventUserCreate = "user_create"
    gitlabWebhookEventUserDestroy = "user_destroy"
    gitlabWebhookEventKeyCreate = "key_create"
    gitlabWebhookEventKeyDestroy = "key_destroy"
    gitlabWebhookEventGroupCreate = "group_create"
    gitlabWebhookEventGroupDestroy = "group_destroy"
    gitlabWebhookEventUserAddToGroup = "user_add_to_group"
    gitlabWebhookEventUserRemoveFromGroup = "user_remove_from_group"
    gitlabWebhookEventPush = "push"
    gitlabWebhookEventTagPush = "tag_push"
