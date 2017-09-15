#!/usr/bin/python2.7
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
import pyotp


def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t

def loginBot():
    try:
        f = open('/root/reddit/sidebar/login.txt')
        fkey = open('/root/reddit/sidebar/2fakey.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect = f.readline().split('||',8)
        key = fkey.readline().rstrip()
        password += ':'+pyotp.TOTP(key).now()
        f.close()
        fkey.close()
        r = praw.Reddit(client_id=id,
             client_secret=secret,
             password=password,
             user_agent=user_agent,
             username=username)
        print getTimestamp() + "OAuth session opened as /u/" + r.user.me().name
        return r,admin,username,password,subreddit,user_agent,id,secret,redirect
    except Exception, e:
        print getTimestamp() + str(e)
        print getTimestamp() + "Setup error \n"
        sleep(10)


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
        r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
	settings = r.subreddit(subreddit).mod.settings()
	contents = settings['description']
	#We want to update current sidebar to where injury table goes
	contents = re.sub('\[\/\/\]: # \(Premier Table\).*\[\/\/\]: # \(End Premier Table\)',eplTable,contents,flags=re.DOTALL)
	r.subreddit(subreddit).mod.update(description=contents)

def updateEuropa():
	europaTable = buildEuropa()		
        r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
	settings = r.subreddit(subreddit).mod.settings()
	contents = settings['description']
	#We want to update current sidebar to where injury table goes
	contents = re.sub('\[\/\/\]: # \(Europa Table\).*\[\/\/\]: # \(End Europa Table\)',europaTable,contents,flags=re.DOTALL)
	r.subreddit(subreddit).mod.update(description=contents)




updateSidebar()
updateEuropa()
print getTimestamp() + "Premier League Table Updated"
