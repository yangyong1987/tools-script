#!/usr/bin/python
#coding:utf-8
#yy 2018.01.11

import requests
import xlsxwriter
import time
import optparse
from gitlabGroup import GroupsData
from gitlabProject import PeojectsData
from gitlabUser import UsersData

class GitlabData(object):
    def __init__(self):
        self.url = "https://git.vankeservice.com"
        self.private_token = "Edb7BZyEKuWWL2n_3UCS"
        #数据最终生成的excel表格
        self.output_xlsx = "output_" + time.strftime("%Y-%m-%d_%H%M%S",time.localtime()) + ".xlsx"

        #初始化对象
        self.workbook = xlsxwriter.Workbook(self.output_xlsx)
        self.groups = GroupsData(self.url, self.private_token)
        self.projects = PeojectsData(self.url, self.private_token)
        self.users = UsersData(self.url, self.private_token)

    #这个方法是将传入的二维数据写入excel
    def WriteXlsx(self, worksheet, dataList, head):
        n = 0
        #excel表格列表序号
        column = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ"]
        #excel首行加粗
        bold= self.workbook.add_format({'bold':True})
        for i in head:
            worksheet.write(column[n] + '1', unicode(i, "utf-8"), bold)
            n = n + 1
        #将传入的二维数据写入excel表格
        for i in range(len(dataList)):
            for j in range(len(head)):
                col = column[j] + str(i + 2)
                #print dataList[i][j]
                try:
                    worksheet.write(col, dataList[i][j])
                except:
                    print "WARNNING!!! ",dataList[i][j],"cannot write in", col
    
    #执行方法，根据传进的参数决定输出部分数据还是全部数据
    def Exec(self, output):
        print "output excel:",self.output_xlsx
        worksheet1 = self.workbook.add_worksheet(self.groups.sheet)
        worksheet2 = self.workbook.add_worksheet(self.projects.sheet)
        worksheet3 = self.workbook.add_worksheet(self.users.sheet)
        self.WriteXlsx(worksheet1, self.groups.dataList, self.groups.head)
        self.WriteXlsx(worksheet2, self.projects.dataList, self.projects.head)
        self.WriteXlsx(worksheet3, self.users.dataList, self.users.head)
        self.workbook.close()
        
def parseages():
    parser = optparse.OptionParser()
    parser.add_option("-o", "--output", dest="output", help="...",default="a")
    (option,args) = parser.parse_args()
    return (option,args)

def main():
    (options, args) = parseages()
    output = options.output.strip()
    gd = GitlabData()
    gd.Exec(output)

if __name__ == '__main__':
    main()