#!/usr/bin/python
#coding:utf-8
#yangy114 2017.12.04
'''
用mail.vanke.com邮件服务器进行邮件发送
'''
import optparse
import os
import smtplib
import sys
import requests
import json
import re
import commands
import platform
import zipfile
import shutil
import chardet
from vkcm_email import VkEmail
from vkcm_email_qq import send_email
from vkcm_email_qq import default_email_config_myqq
from vkcm_email_qq import default_email_config_vanke

def get_body(project, build_num, build_status, log_add, build_add, changeHtml):
    
    body = '''
<html>
 <head></head> 
 <body> 
  <p><strong>本邮件是程序自动下发的，请勿回复！！！</strong></p> 
  <style>
        table {border-color:#000000; border-collapse:collapse;font-size:12px}   
    </style> 
  <table border="1" align="center" cellpadding="5" cellspacing="0" width="100%%"> 
   <tbody> 
    <tr> 
     <th style="background:#2674a6;color:#FFFFFF;font-size:16px" bgcolor="#EDF3FE" width="130" height="40">项目</th> 
     <th style="background:#2674a6;color:#FFFFFF;font-size:16px" colspan="2">数据</th> 
    </tr> 
    <tr> 
     <td>Jenkins Job</td> 
     <td colspan="2">%s</td> 
    </tr> 
    <tr> 
     <td>构建编号</td> 
     <td  colspan="2">第%s次构建第</td> 
    </tr> 
    <tr> 
     <td>构建状态</td> 
     <td colspan="2">%s</td> 
    </tr> 
    <tr> 
     <td>构建日志地址</td> 
     <td colspan="2">%s</td> 
    </tr> 
    <tr> 
     <td>构建地址</td> 
     <td  colspan="2">%s</td> 
    </tr> 
    %s
   </tbody> 
  </table>   
 </body>
</html>''' % (project, build_num, build_status, log_add, build_add, changeHtml)
    return body

def get_git_info(pre_reversion, reversion):
    giturl = "https://vk_cmo:vk_cmo234@git.vankeservice.com/RDManagement/Ares-vanke/ATS/ats.git"
    gitbranch = "master"
    print "pre_reversion:",pre_reversion
    print "reversion",reversion
    if os.path.exists("code"):
        shutil.rmtree("code")
    _cmd = "git clone %s code -b %s" % (giturl, gitbranch)
    os.system(_cmd)
    os.chdir("code")
    gitlog_cmd = "git log --no-merges --pretty=\"(%%h)(%%ci) %%an|||%%s\" %s...%s" % (pre_reversion, reversion)
    #print gitlog_cmd
    gitlogall_cmd = "git log %s...%s" % (pre_reversion, reversion)
    logstatus, _log = commands.getstatusoutput(gitlog_cmd)
    alllogstatus, _alllog = commands.getstatusoutput(gitlogall_cmd)
    #print "_log",_log
    logline = re.split("\n", _log)
    
    changeHtml = ""
    n = 0
    for i in logline:
        loghead = i.split("|||")[0][0:26]+i.split("|||")[0][35:]
        if n == 0:
            changeHtml = '''<tr><td width="130" rowspan="%d">变更集</td><td width="20%%">%s</td><td>%s</td></tr>''' % (len(logline), loghead, i.split("|||")[1])
            n = 1
        else:
            changeHtml = changeHtml + '''<tr><td width="20%%">%s</td><td>%s</td></tr>''' % (loghead, i.split("|||")[1])

    #build_plat = platform.system()
    #print build_plat
    #if build_plat == "Linux":
    #    ver_file = "src/main/resources/mysql-config.properties"
    #elif build_plat == "Windows":
    #    ver_file = r"src\main\resources\mysql-config.properties"
    #else:
    #    ver_file = None
    #if ver_file is not None:
    #    the_text = open(ver_file).read()
    #    version_num = re.search(r'(.*)serverVersion=(.*)', the_text).group(2)
    #else:
    #    version_num = "sorry,cannot find version number."
    #print "version_num:",version_num
    #slog = ""
    #try:
    #    jira_issue_id_list = re.findall(r'#(BLACKCAT2-\d+);', _alllog)
    #    for j in jira_issue_id_list:
    #        slog = slog + j + ","
    #except:
    #    jira_issue_id_list = ["jira单号查找异常"]
    return changeHtml

def parseages():
    parser = optparse.OptionParser()
    parser.add_option("", "--header", dest="header", help="email header")
    parser.add_option("", "--job_name", dest="job_name", help="job_name")
    parser.add_option("", "--to_addr", dest="to_addr", help="email to addr list,split with ;")
    parser.add_option("", "--attachment", dest="attachment", help="attachment file,default null",default=None)
    (option,args) = parser.parse_args()
    return (option,args)

def main():
    (options, args) = parseages()
    header = options.header.strip()
    job_name = options.job_name.strip()
    to_addr = options.to_addr.strip()
    attachment = options.attachment
    jenkins_url = "http://10.0.75.85:8082"

    url_job = "%s/job/%s/api/json?pretty=true" % (jenkins_url, job_name)
    r = requests.get(url_job)
    project = r.json()["displayName"].encode("gbk")
    build_num = r.json()["lastBuild"]["number"]
    build_url = r.json()["url"].encode("gbk")
    print "project:",project
    print "build_num:",build_num
    print "build_url:", build_url

    url_log = "%s/job/%s/%s/api/json?pretty=true" % (jenkins_url, job_name, build_num)
    r_log = requests.get(url_log)
    log_url = "%s/job/%s/%s/consoleText" % (jenkins_url, job_name, build_num)
    build_status = r_log.json()["result"].encode("gbk")

    git_url = "%s/job/%s/%s/git/api/json?pretty=true" % (jenkins_url, job_name, build_num)
    r_git = requests.get(git_url)
    reversion = r_git.json()["lastBuiltRevision"]["SHA1"]

    if build_num == 1:
        pre_build_num = build_num
    else:
        pre_build_num = build_num - 1
        pre_reversion_flag = 0
        while pre_reversion_flag != 1:
            pre_git_url = "%s/job/%s/%s/git/api/json?pretty=true" % (jenkins_url, job_name, pre_build_num)
            print "pre_git_url",pre_git_url
            try:
                pre_r_git = requests.get(pre_git_url)
                pre_url = "%s/job/%s/%s/api/json?pretty=true" % (jenkins_url, job_name, pre_build_num)
                pre_json = requests.get(pre_url)
                pre_build_status = pre_json.json()["result"].encode("gbk")
                print "fine in #",pre_build_num, pre_build_status                
            except:
                pre_build_status = ""
            if pre_build_status != "SUCCESS":
                pre_build_num = pre_build_num - 1
            else:
                pre_reversion_flag = 1
                pre_reversion = pre_r_git.json()["lastBuiltRevision"]["SHA1"]
    print "lastSuccessfulBuildId:",pre_build_num

    change = get_git_info(pre_reversion,reversion)

    body = get_body(project, build_num, build_status, log_url, build_url, change)
    
    subject = build_status + ":自动化测试平台:" + project + " " + header
    
    #attachment = None
    to_addr_list = re.split(",|;", to_addr)
    if attachment is not None:
        if build_status == "SUCCESS":
            attachment = re.split(",|;", attachment)
        else:
            attachment = None
    from_addr, displayname, password, smtp_server, smtp_port, transport = default_email_config_vanke()
    send_email(from_addr, displayname, password, to_addr_list, smtp_server, smtp_port, transport, subject, body, attachment)

if __name__ == '__main__':
    sys.stdout = sys.stderr
    main()
