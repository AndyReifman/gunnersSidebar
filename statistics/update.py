#!/usr/bin/python3
"""
' Andrew Reifman-Packett
' May 2017
"""
import getGoals
import getAssists
import praw
import datetime
import re
from time import sleep

def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + minute + '] '
    return dt + t

def loginBot():
    try:
        f = open('/home/andy/reddit/sidebar/login.txt')
        subreddit,user_agent,client_id,secret,refresh = f.readline().split('||', 8)
        f.close()
        r = praw.Reddit(client_id=client_id,
                        client_secret=secret,
                        refresh_token=refresh.strip(),
                        user_agent=user_agent)
        print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
        return r,subreddit
    except Exception as e:
        print(getTimestamp() + str(e))
        print(getTimestamp() + "Setup error in statistics\n")
        sleep(5)
        exit()

def buildGoalSidebar():
    body = "[//]: # (Goals Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += getGoals.main()
    body += "[//]: # (End Goals Table)"
    return body

def buildAssistsSidebar():
    body = "[//]: # (Assists Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += getAssists.main()
    body += "[//]: # (End Assists Table)"
    return body


def updateGoals():
    goals = buildGoalSidebar()
    assists = buildAssistsSidebar()
    r,subreddit = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Goals Table\).*\[\/\/\]: # \(End Goals Table\)',goals,contents,flags=re.DOTALL)
    contents = re.sub('\[\/\/\]: # \(Assists Table\).*\[\/\/\]: # \(End Assists Table\)',assists,contents,flags=re.DOTALL)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)



updateGoals()
print(getTimestamp() + "Goals Table Updated")
print(getTimestamp() + "Assists Table Updated")
