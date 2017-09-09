#!/usr/bin/python2.7
'''
' Andrew Reifman-Packett
' May 2017
'''
import findMatches
import praw
import datetime
import time
import re
from time import sleep


def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t

def loginBot():
    try:
        f = open('/root/reddit/sidebar/login.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect = f.readline().split('||',8)
        f.close()
        r = praw.Reddit(client_id=id,
             client_secret=secret,
             password=password,
             user_agent=user_agent,
             username=username)
        print getTimestamp() + "OAuth session opened as /u/" + r.user.me().name
        return r,admin,username,password,subreddit,user_agent,id,secret,redirect
    except:
                print getTimestamp() + "Setup error \n"
                sleep(10)






def buildSidebar():
    body = "[//]: # (Fixtures Table)\n"
    body += "| Date | Result/Time | Opponent | [](#icon-trophy) |\n"
    body += "|:----:|:----:|:----:|:----:|\n"
    body += findMatches.main()
    body += "[//]: # (End Fixtures Table)"
    return body

def updateResults():
    results = buildSidebar()
    r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
    #r = loginBot()
    #settings = r.get_settings('gunners')
    #settings = r.settings()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Fixtures Table\).*\[\/\/\]: # \(End Fixtures Table\)',results,contents,flags=re.DOTALL)
    #r.update_settings(r.get_subreddit("jacktest"),description=contents)
    r.subreddit(subreddit).mod.update(description=contents)



updateResults()
print getTimestamp() + "Fixtures & Results Table Updated"
