#!/usr/bin/python2.7
# coding: utf-8
from unidecode import unidecode
from time import sleep
import requests
import datetime
import time
import re
import praw
import pyotp

item = dict()
f = open('/root/reddit/sidebar/injury/api.txt')
apiKey = f.readline().splitlines()[0]
#Get the injury list from arsenalreport.com
def getInjuries():
	resp = requests.get('https://www.arsenalreport.com/v1/injuries?api_key='+apiKey)
	try:
		for item in resp.json():
			#Print out ongoing injuries
	 		if item['end_date'] == None:
				injury = item['injury_type']
				injury = re.sub('\(([^\)]+)\)', '',injury)
				time = item['expected_return']
				if time == 0:
					time = "Unknown"
			 		#print item['player']['first_name'] + " " + item['player']['last_name'] + ": " + injury + " Unknown"
				#else:
			 		#print item['player']['first_name'] + " " + item['player']['last_name'] + ": " + injury + " " + str(time) + " weeks"
	except:
		print "Bad Request"

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
        if str(e) == 'invalid_grant error processing request':
            loginBot()
            return
        print getTimestamp() + "Setup error \n"
        sleep(10)

def buildSidebar():
	injUrl = "http://www.arsenal.com/first-team/players/"
	resp = requests.get('https://www.arsenalreport.com/v1/injuries?api_key='+apiKey)
	body = "[//]: # (Injury Table)\n"
	body += "| Player | Injury | Estimated Return |\n"
	body += "|:------:|:-------:|:---------:|\n"
	for item in resp.json():
		#Print out ongoing injuries
 		if item['end_date'] == None:
			injury = item['injury_type']
			injury = re.sub('\(([^\)]+)\)', '',injury)
			time = item['expected_return']
                        if unidecode(item['player']['first_name'].lower()) == "gabriel":
                           playerUrl = "http://www.arsenal.com/first-team/players/gabriel"
                        else:
                            playerUrl = "http://www.arsenal.com/first-team/players/" + unidecode(item['player']['first_name'].lower()) + "-"+ unidecode(item['player']['last_name'].lower())
			body += "|[" + item['player']['first_name'] + " " + item['player']['last_name'] + "](" + playerUrl + ")|" + injury + "|" + str(time) + "|\n"
	body += "[//]: # (End Injury Table)"
	return body


#Update the sidebar
def updateSidebar():
	injTable = buildSidebar()		
        r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
	settings = r.subreddit(subreddit).mod.settings()
	contents = settings['description']
	#We want to update current sidebar to where injury table goes
	contents = re.sub('\[\/\/\]: # \(Injury Table\).*\[\/\/\]: # \(End Injury Table\)',injTable,contents,flags=re.DOTALL)
	r.subreddit(subreddit).mod.update(description=contents)




getInjuries()
updateSidebar()
print getTimestamp() + "Injury Table Updated"
