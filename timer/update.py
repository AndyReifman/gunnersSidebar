#!/usr/bin/python3
from __future__ import print_function
import datetime
import time
<<<<<<< HEAD
=======
import pyotp
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
import praw
import re
import postThread
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
createThread = 0

def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t


def loginBot():
    try:
<<<<<<< HEAD
        f = open('/home/andy/reddit/sidebar/login.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect,refresh = f.readline().split('||',8)
        f.close()
=======
        f = open('/root/reddit/sidebar/login.txt')
        fkey = open('/root/reddit/sidebar/2fakey.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect,refresh = f.readline().split('||',8)
        key = fkey.readline().rstrip()
        totp = pyotp.TOTP(key)
        password += ':'+totp.now()
        f.close()
        fkey.close()
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
        r = praw.Reddit(client_id=id,
             client_secret=secret,
             refresh_token=refresh.strip(),
             user_agent=user_agent)
        print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
        return r,admin,username,password,subreddit,user_agent,id,secret,redirect
    except (Exception, e):
        print(getTimestamp() + str(e))
        if str(e) == 'invalid_grant error processing request':
            print(getTimestamp() + 'Attempting to log in again.\n')
            time.sleep(5)
            loginBot()
            return
        print(getTimestamp() + "Setup error \n")


def main():
<<<<<<< HEAD
    store = file.Storage('/home/andy/reddit/sidebar/timer/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/andy/reddit/sidebar/timer/credentials.json', SCOPES)
=======
    store = file.Storage('/root/reddit/sidebar/timer/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/root/reddit/sidebar/timer/credentials.json', SCOPES)
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    #printEvents(service)
    #Get the countdown
    countdown = arsenal(service)
    body = ">>>>>\n"
    body += "#### Next game in: " +countdown +"\n"
    body += ">>>>>"
    #Login
    r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    #Get Sidebar
    contents = settings['description']
    #update Timer#
    contents = re.sub('>>>>>.*>>>>>',body,contents,flags=re.DOTALL)
    #r.subreddit(subreddit).mod.update(description=contents)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)
    return



def arsenal(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='6umq7as3vved7j286f88lk7c14@group.calendar.google.com', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    now = datetime.datetime.utcnow()

    if not events:
        print('No upcoming events found.')
        return "None Scheduled"
    for event in events:
        global summary
        summary = event['summary']
        start = event['start'].get('dateTime', event['start'].get('date'))
        pattern = '%Y-%m-%dT%H:%M:%SZ'
        epoch = int(time.mktime(time.strptime(start,pattern)))
        diff = epoch - int(now.timestamp())
        date = datetime.timedelta(seconds=diff)
        if '-1 day' in str(date):
            return "Now!"
        global matchDate 
        matchDate = start.split('T')[0]

        return convert(str(date))

def convert(timeStamp):
    try: 
        days = timeStamp.split(' ')[0] + ' days '
        temp = timeStamp.split(',')[1].strip()
    except:
        days = '0 days '
        temp = timeStamp
    hours = temp.split(':')[0].strip() + ' hours '
    if days == '0 days ':
<<<<<<< HEAD
        f = open('/home/andy/reddit/sidebar/timer/lockfile')
=======
        f = open('/root/reddit/sidebar/timer/lockfile')
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
        status = f.readline().strip()
        f.close
        now = datetime.datetime.utcnow()
        if now.hour == 8 and status == 'UNLOCKED':
            #We want to create a thread assuming this is the first time around.
            postThread.main(summary,matchDate)
            print("Locking file")
<<<<<<< HEAD
            f = open('/home/andy/reddit/sidebar/timer/lockfile','w')
=======
            f = open('/root/reddit/sidebar/timer/lockfile','w')
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
            f.write('LOCKED')
            f.close()
    else:
        print("Unlocking file")
<<<<<<< HEAD
        f = open('/home/andy/reddit/sidebar/timer/lockfile','w')
=======
        f = open('/root/reddit/sidebar/timer/lockfile','w')
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
        f.write('UNLOCKED')
        f.close()
    minutes = temp.split(':')[1].strip() + ' minutes'
    
    return days + hours + minutes



if __name__ == '__main__':
    main()
