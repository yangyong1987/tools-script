#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests

from gitlabProjectFields import GitlabProjectFields
from gitlabUserFields import GitlabUserFields

class PeojectsData(object):
    def __init__(self, url, private_token):
        self.url = url
        self.private_token = private_token
        #excel的表格名称
        self.sheet = "projects"
        #excel首行标题
        self.head = ["id", \
                     "name", \
                     "description", \
                     "name_with_namespace", \
                     "path", \
                     "path_with_namespace", \
                     "created_at", \
                     "default_branch", \
                     "tag_list", \
                     "ssh_url_to_repo", \
                     "http_url_to_repo", \
                     "web_url", \
                     "star_count", \
                     "forks_count", \
                     "last_activity_at", \
                     "archived", \
                     "visibility", \
                     "resolve_outdated_diff_discussions", \
                     "container_registry_enabled", \
                     "issues_enabled", \
                     "merge_requests_enabled", \
                     "wiki_enabled", \
                     "jobs_enabled", \
                     "snippets_enabled", \
                     "shared_runners_enabled", \
                     "lfs_enabled", \
                     "creator_id", \
                     "namespace_id", \
                     "namespace_name", \
                     "namespace_path", \
                     "namespace_kind", \
                     "namespace_full_path", \
                     "namespace_parent_id", \
                     "import_status", \
                     "import_error", \
                     "open_issues_count", \
                     "runners_token", \
                     "public_jobs", \
                     "ci_config_path", \
                     "shared_with_groups", \
                     "only_allow_merge_if_pipeline_succeeds", \
                     "request_access_enabled", \
                     "only_allow_merge_if_all_discussions_are_resolved", \
                     "printing_merge_request_link_enabled", \
                     "permissions_project_access_access_level", \
                     "permissions_project_access_notification_level", \
                     "permissions_group_access_access_level",\
                     "permissions_group_access_notification_level"]
        self.dataList = self._get_datalist()
    
    def _get_datalist(self):
        flag = True
        m = 0
        #每页50个数据
        perPage = 50
        #页码
        page = 0
        projects_data_list = []
        projects_id_list = []
        while flag:
            page = page + 1
            projects_api_url = "%s/api/v4/projects?private_token=%s&per_page=%s&page=%s" % (self.url, self.private_token, perPage, str(page))
            re = requests.get(projects_api_url)
            data = re.json()
            if data == []:
                flag = False
            else:
                for i in range(len(data)):
                    ps = GitlabProjectFields(data[i])
                    projects_id_list.append(ps.id)
        for i in projects_id_list:
            m = m + 1
            project_user = ""
            project_api_url = "%s/api/v4/projects/%s?private_token=%s&per_page=%s&page=%s" % (self.url, i, self.private_token, perPage, str(m))
            re_project = requests.get(project_api_url)
            project_data = re_project.json()
            p = GitlabProjectFields(project_data)
            project_members_aip_url = "%s/api/v4/projects/%s/members?private_token=%s" % (self.url, i, self.private_token)
            re_project_members = requests.get(project_members_aip_url)
            project_members_data = re_project_members.json()
            #未完
            for j in project_members_data:
                user = GitlabUserFields(j)
                project_user = project_user + user.name + user.username + ","
            projects_data_list.append([p.id, \
                                       p.name, \
                                       p.description, \
                                       p.name_with_namespace, \
                                       p.path, \
                                       p.path_with_namespace, \
                                       p.created_at, \
                                       p.default_branch, \
                                       p.tag_list, \
                                       p.ssh_url_to_repo, \
                                       p.http_url_to_repo, \
                                       p.web_url, \
                                       p.star_count, \
                                       p.forks_count, \
                                       p.last_activity_at, \
                                       p.archived, \
                                       p.visibility, \
                                       p.resolve_outdated_diff_discussions, \
                                       p.container_registry_enabled, \
                                       p.issues_enabled, \
                                       p.merge_requests_enabled, \
                                       p.wiki_enabled, \
                                       p.jobs_enabled, \
                                       p.snippets_enabled, \
                                       p.shared_runners_enabled, \
                                       p.lfs_enabled, \
                                       p.creator_id, \
                                       p.namespace_id, \
                                       p.namespace_name, \
                                       p.namespace_path, \
                                       p.namespace_kind, \
                                       p.namespace_full_path, \
                                       p.namespace_parent_id, \
                                       p.import_status, \
                                       p.import_error, \
                                       p.open_issues_count, \
                                       p.runners_token, \
                                       p.public_jobs, \
                                       p.ci_config_path, \
                                       p.shared_with_groups, \
                                       p.only_allow_merge_if_pipeline_succeeds, \
                                       p.request_access_enabled, \
                                       p.only_allow_merge_if_all_discussions_are_resolved, \
                                       p.printing_merge_request_link_enabled, \
                                       p.permissions_project_access_access_level, \
                                       p.permissions_project_access_notification_level, \
                                       p.permissions_group_access_access_level, \
                                       p.permissions_group_access_notification_level])

        return projects_data_list
