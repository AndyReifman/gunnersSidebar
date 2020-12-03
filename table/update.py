#!/usr/bin/python3
import getTable
import europaTable
from unidecode import unidecode
from pprint import pprint
import requests
import datetime
import time
from time import sleep
import re
import praw
import sys
import traceback


def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t

def loginBot():
    try:
        f = open('/home/andy/reddit/sidebar/login.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect,refresh = f.readline().split('||',8)
        f.close()
        r = praw.Reddit(client_id=id,
             client_secret=secret,
             refresh_token=refresh.strip(),
             user_agent=user_agent)
        print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
        return r,admin,username,password,subreddit,user_agent,id,secret,redirect
    except Exception as e:
        print(getTimestamp() + str(e))
        print(getTimestamp() + "Setup error in Table \n")
        time.sleep(5)
        exit()


def buildSidebar():
    body = "[//]: # (Premier Table)\n"
    body += "|\\#| Team | GD | Points \n"
    body += "|::|:-:|:--:|:--:|\n"
    body += getTable.main()
    body += "[//]: # (End Premier Table)"
    return body

def buildEuropa():
     body = "[//]: # (Europa Table)\n"
     body += "|\\#| Team | GD | Points \n"
     body += "|::|:-:|:--:|:--:|\n"
     body += europaTable.main()
     body += "[//]: # (End Europa Table)"
     return body


#Update the sidebar
def updateSidebar():
    eplTable = buildSidebar()		
    #europaTable = buildEuropa()		
    r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
	#We want to update current sidebar to where injury table goes
    contents = re.sub('\[\/\/\]: # \(Premier Table\).*\[\/\/\]: # \(End Premier Table\)',eplTable,contents,flags=re.DOTALL)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)
    print(getTimestamp() + "Premier League Table Updated")

updateSidebar()
