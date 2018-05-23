#!/usr/bin/python
#coding:utf-8
#yangyong1 2018.05.21
#
# https://msdn.microsoft.com/zh-cn/vba/vba-powerpoint

import sys
import os
import glob
import shutil
import subprocess
from pptx import Presentation
import win32com.client
import win32com.client.dynamic
import time
import glob

class zbpptx(object):
    def __init__(self):
        self.ltime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        t1 = unicode("研发中心周会_分组版_", "utf-8")
        t2 = unicode("研发中心周会_时间版_", "utf-8")
        self.pptMergeByTime = t1 + self.ltime + ".pptx"
        self.pptMergeByGroup = t2 + self.ltime + ".pptx"
        shutil.copyfile("init.pptx",self.pptMergeByTime)
        shutil.copyfile("init.pptx",self.pptMergeByGroup)
        self.other_department = "other_department.pptx"

    def Exec(self):
        sub_amss_list = glob.glob("p*.pptx")
        for i in sub_amss_list:
            print i.decode('gb2312')
        self.GreatPPTMergeByTime(sub_amss_list)
        self.GreatPPTMergeByGroup(sub_amss_list)

    #按时间顺序生成ppt    
    def GreatPPTMergeByTime(self, files):
        Application = win32com.client.Dispatch("PowerPoint.Application")
        Application.Visible = True
        ppt = os.path.join(os.getcwd(), self.pptMergeByTime)
        new_ppt = Application.Presentations.Open(ppt)
        for f in files:
            exit_ppt = Application.Presentations.Open(os.path.join(os.getcwd(), f))
            page_num = exit_ppt.Slides.Count
            exit_ppt.Close()
            new_ppt.Slides.InsertFromFile(os.path.join(os.getcwd(), f),new_ppt.Slides.Count,1,page_num)
        new_ppt.Slides.InsertFromFile(os.path.join(os.getcwd(), self.other_department),new_ppt.Slides.Count,1,2)
        Application.Presentations(1).SaveAs(ppt)
        Application.Presentations(ppt).Close
        Application.Quit()

    #按业务组顺序生成ppt    
    def GreatPPTMergeByGroup(self, files):
        Application = win32com.client.Dispatch("PowerPoint.Application")
        Application.Visible = True
        ppt = os.path.join(os.getcwd(), self.pptMergeByGroup)
        new_ppt = Application.Presentations.Open(ppt)
        for f in files:
            exit_ppt = Application.Presentations.Open(os.path.join(os.getcwd(), f))
            page_num = exit_ppt.Slides.Count
            exit_ppt.Close()
            new_ppt.Slides.InsertFromFile(os.path.join(os.getcwd(), f),new_ppt.Slides.Count,1,page_num-1)
        for f in files:
            exit_ppt = Application.Presentations.Open(os.path.join(os.getcwd(), f))
            page_num = exit_ppt.Slides.Count
            exit_ppt.Close()
            new_ppt.Slides.InsertFromFile(os.path.join(os.getcwd(), f),new_ppt.Slides.Count,page_num,page_num) 
        new_ppt.Slides.InsertFromFile(os.path.join(os.getcwd(), self.other_department),new_ppt.Slides.Count,1,2)
        Application.Presentations(1).SaveAs(ppt)
        Application.Presentations(ppt).Close
        Application.Quit()     

def main():
    a = zbpptx()
    a.Exec()
    
if __name__ == '__main__':
    main()