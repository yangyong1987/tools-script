#!/usr/bin/python
# coding:utf-8
#yangy114 2017-12-14

from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
import json
from vkwebhooks.jira.vkJirasd2Jira import Jirasd2Jira
from vkwebhooks.jira.vkJira2Jirasd import Jira2Jirasd
from vkwebhooks.gitlab.gitlabManage import vkgitlab

def main():
    app = Flask(__name__)

    @app.route('/test' , methods=['GET', 'POST'])
    def run_test():
        if request.method == 'POST':
            data = request.get_data()
            dataDict = json.loads(data)
            print "\n ==test=== \n"
            Jirasd2Jira(dataDict)
            #print json.dumps(dataDict)
            return str(json.dumps(dataDict))
        else:
            return '<h1>只接受post请求！</h1>'

    @app.route('/jira' , methods=['GET', 'POST'])
    def run_jira():
        if request.method == 'POST':
            data = request.get_data()
            dataDict = json.loads(data)
            print "\n ==jira=== \n"
            Jira2Jirasd(dataDict)
            return str(json.dumps(dataDict))
        else:
            return '<h1>只接受post请求！</h1>'

    @app.route('/jirasd' , methods=['GET', 'POST'])
    def run_jirasd():
        if request.method == 'POST':
            data = request.get_data()
            dataDict = json.loads(data)
            print "\n ==jirasd=== \n"
            Jirasd2Jira(dataDict)
            return str(json.dumps(dataDict))
        else:
            return '<h1>只接受post请求！</h1>'

    @app.route('/gitlab' , methods=['GET', 'POST'])
    def run_gitlab():
        if request.method == 'POST':
            data = request.get_data()
            dataDict = json.loads(data)
            print "\n ==gitlab=== \n"
            vkgitlab(dataDict)
            return str(json.dumps(dataDict))
        else:
            return '<h1>只接受post请求！</h1>'

    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()