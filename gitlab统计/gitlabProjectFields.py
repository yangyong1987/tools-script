#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests

class GitlabProjectFields(object):
    def __init__(self, projectdata):
        #print projectdata
        self.id, \
        self.description, \
        self.name, \
        self.name_with_namespace, \
        self.path, \
        self.path_with_namespace, \
        self.created_at, \
        self.default_branch, \
        self.tag_list, \
        self.ssh_url_to_repo, \
        self.http_url_to_repo, \
        self.web_url, \
        self.star_count, \
        self.forks_count, \
        self.last_activity_at, \
        self.archived, \
        self.visibility, \
        self.resolve_outdated_diff_discussions, \
        self.container_registry_enabled, \
        self.issues_enabled, \
        self.merge_requests_enabled, \
        self.wiki_enabled, \
        self.jobs_enabled, \
        self.snippets_enabled, \
        self.shared_runners_enabled, \
        self.lfs_enabled, \
        self.creator_id, \
        self.namespace_id, \
        self.namespace_name, \
        self.namespace_path, \
        self.namespace_kind, \
        self.namespace_full_path, \
        self.namespace_parent_id, \
        self.import_status, \
        self.import_error, \
        self.open_issues_count, \
        self.runners_token, \
        self.public_jobs, \
        self.ci_config_path, \
        self.shared_with_groups, \
        self.only_allow_merge_if_pipeline_succeeds, \
        self.request_access_enabled, \
        self.only_allow_merge_if_all_discussions_are_resolved, \
        self.printing_merge_request_link_enabled, \
        self.permissions_project_access_access_level, \
        self.permissions_project_access_notification_level, \
        self.permissions_group_access_access_level, \
        self.permissions_group_access_notification_level = self._GetProjectInfo(projectdata)
        
    def _GetProjectInfo(self, data):
        try:
            id = data["id"]
        except:
            id = ""
        try:
            description = data["description"]
        except:
            description = ""
        try:
            name = data["name"]
        except:
            name = ""
        try:
            name_with_namespace = data["name_with_namespace"]
        except:
            name_with_namespace = ""
        try:
            path = data["path"]
        except:
            path = ""
        try:
            path_with_namespace = data["path_with_namespace"]
        except:
            path_with_namespace = ""
        try:
            created_at = data["created_at"]
        except:
            created_at = ""
        try:
            default_branch = data["default_branch"]
        except:
            default_branch = ""
        try:
            #待修改
            tag_list = ""
        except:
            tag_list = ""
        try:
            ssh_url_to_repo = data["ssh_url_to_repo"]
        except:
            ssh_url_to_repo = ""
        try:
            http_url_to_repo = data["http_url_to_repo"]
        except:
            http_url_to_repo = ""
        try:
            web_url = data["web_url"]
        except:
            web_url = ""
        try:
            star_count = data["star_count"]
        except:
            star_count = ""
        try:
            forks_count = data["forks_count"]
        except:
            forks_count = ""
        try:
            last_activity_at = data["last_activity_at"]
        except:
            last_activity_at = ""
        try:
            archived = data["archived"]
        except:
            archived = ""
        try:
            visibility = data["visibility"]
        except:
            visibility = ""
        try:
            resolve_outdated_diff_discussions = data["resolve_outdated_diff_discussions"]
        except:
            resolve_outdated_diff_discussions = ""
        try:
            container_registry_enabled = data["container_registry_enabled"]
        except:
            container_registry_enabled = ""
        try:
            issues_enabled = data["issues_enabled"]
        except:
            issues_enabled = ""
        try:
            merge_requests_enabled = data["merge_requests_enabled"]
        except:
            merge_requests_enabled = ""
        try:
            wiki_enabled = data["wiki_enabled"]
        except:
            wiki_enabled = ""
        try:
            jobs_enabled = data["jobs_enabled"]
        except:
            jobs_enabled = ""
        try:
            snippets_enabled = data["snippets_enabled"]
        except:
            snippets_enabled = ""
        try:
            shared_runners_enabled = data["shared_runners_enabled"]
        except:
            shared_runners_enabled = ""
        try:
            lfs_enabled = data["lfs_enabled"]
        except:
            lfs_enabled = ""
        try:
            creator_id = data["creator_id"]
        except:
            creator_id = ""
        try:
            namespace_id = data["namespace"]["id"]
        except:
            namespace_id = ""
        try:
            namespace_name = data["namespace"]["name"]
        except:
            namespace_name = ""
        try:
            namespace_path = data["namespace"]["path"]
        except:
            namespace_path = ""
        try:
            namespace_kind = data["namespace"]["kind"]
        except:
            namespace_kind = ""
        try:
            namespace_full_path = data["namespace"]["full_path"]
        except:
            namespace_full_path = ""
        try:
            namespace_parent_id = data["namespace"]["parent_id"]
        except:
            namespace_parent_id = ""
        try:
            import_status = data["import_status"]
        except:
            import_status = ""
        try:
            import_error = data["import_error"]
        except:
            import_error = ""
        try:
            open_issues_count = data["open_issues_count"]
        except:
            open_issues_count = ""
        try:
            runners_token = data["runners_token"]
        except:
            runners_token = ""
        try:
            public_jobs = data["public_jobs"]
        except:
            public_jobs = ""
        try:
            ci_config_path = data["ci_config_path"]
        except:
            ci_config_path = ""
        try:
            #待修改
            shared_with_groups = ""
        except:
            shared_with_groups = ""
        try:
            only_allow_merge_if_pipeline_succeeds = data["only_allow_merge_if_pipeline_succeeds"]
        except:
            only_allow_merge_if_pipeline_succeeds = ""
        try:
            request_access_enabled = data["request_access_enabled"]
        except:
            request_access_enabled = ""
        try:
            only_allow_merge_if_all_discussions_are_resolved = data["only_allow_merge_if_all_discussions_are_resolved"]
        except:
            only_allow_merge_if_all_discussions_are_resolved = ""
        try:
            printing_merge_request_link_enabled = data["printing_merge_request_link_enabled"]
        except:
            printing_merge_request_link_enabled = ""
        try:
            permissions_project_access_access_level = data["permissions"]["project_access"]["access_level"]
        except:
            permissions_project_access_access_level = ""
        try:
            permissions_project_access_notification_level = data["permissions"]["project_access"]["notification_level"]
        except:
            permissions_project_access_notification_level = ""
        try:
            permissions_group_access_access_level = data["permissions"]["group_access"]["access_level"]
        except:
            permissions_group_access_access_level = ""
        try:
            permissions_group_access_notification_level = data["permissions"]["group_access"]["notification_level"]
        except:
            permissions_group_access_notification_level = ""

        
        return id, \
               description, \
               name, \
               name_with_namespace, \
               path, \
               path_with_namespace, \
               created_at, \
               default_branch, \
               tag_list, \
               ssh_url_to_repo, \
               http_url_to_repo, \
               web_url, \
               star_count, \
               forks_count, \
               last_activity_at, \
               archived, \
               visibility, \
               resolve_outdated_diff_discussions, \
               container_registry_enabled, \
               issues_enabled, \
               merge_requests_enabled, \
               wiki_enabled, \
               jobs_enabled, \
               snippets_enabled, \
               shared_runners_enabled, \
               lfs_enabled, \
               creator_id, \
               namespace_id, \
               namespace_name, \
               namespace_path, \
               namespace_kind, \
               namespace_full_path, \
               namespace_parent_id, \
               import_status, \
               import_error, \
               open_issues_count, \
               runners_token, \
               public_jobs, \
               ci_config_path, \
               shared_with_groups, \
               only_allow_merge_if_pipeline_succeeds, \
               request_access_enabled, \
               only_allow_merge_if_all_discussions_are_resolved, \
               printing_merge_request_link_enabled, \
               permissions_project_access_access_level, \
               permissions_project_access_notification_level, \
               permissions_group_access_access_level, \
               permissions_group_access_notification_level
