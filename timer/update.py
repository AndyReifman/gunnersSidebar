#!/usr/bin/python3
from __future__ import print_function

import datetime
import os
import re
import time

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from onebag import login_bot

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
createThread = 0


def main():
    store = file.Storage('/home/andy/reddit/sidebar/timer/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/andy/reddit/sidebar/timer/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    # printEvents(service)
    # Get the countdown
    countdown = arsenal(service)
    body = ">>>>>\n"
    body += "#### Next game in: " + countdown + "\n"
    body += ">>>>>"
    # Login
    r, subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    settings = r.subreddit(subreddit).mod.settings()
    # Get Sidebar
    contents = settings['description']
    # update Timer#
    contents = re.sub('>>>>>.*>>>>>', body, contents, flags=re.DOTALL)
    # r.subreddit(subreddit).mod.update(description=contents)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)
    return


def arsenal(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='6umq7as3vved7j286f88lk7c14@group.calendar.google.com',
                                          timeMin=now,
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
        epoch = int(time.mktime(time.strptime(start, pattern)))
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
    minutes = temp.split(':')[1].strip() + ' minutes'

    return days + hours + minutes


if __name__ == '__main__':
    main()
