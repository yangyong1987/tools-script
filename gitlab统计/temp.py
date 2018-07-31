#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

l = ["id", \
"description", \
"name", \
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
"permissions_project_access", \
"permissions_group_access_access_level", \
"permissions_group_access_notification_level"
]

for i in l:
    a = '''
    try:
        %s = data["%s"]
    except:
        %s = ""
    ''' % (i,i,i)
    print a
