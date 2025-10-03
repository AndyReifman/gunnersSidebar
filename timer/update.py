#!/usr/bin/python3
from __future__ import print_function

import os
import re
import requests
import pytz

from datetime import datetime 
from icalendar import Calendar
from onebag import login_bot

CALENDAR_URL = "https://calendar.google.com/calendar/ical/6umq7as3vved7j286f88lk7c14%40group.calendar.google.com/public/basic.ics"

createThread = 0

def get_next_events():
    try:
        print("Fetching eCal data...")
        response = requests.get(CALENDAR_URL)
        response.raise_for_status()

        gcal = Calendar.from_ical(response.text)

        events = []
        now = datetime.now(pytz.utc)

        for component in gcal.walk():
            if component.name == "VEVENT":
                start_dt = component.get('dtstart').dt

                if isinstance(start_dt, datetime):
                    if start_dt.tzinfo is None or start_dt.tzinfo.utcoffset(start_dt) is None:
                        start_dt = pytz.utc.localize(start_dt)
                end_dt = component.get('dtend').dt
                if isinstance(end_dt, datetime):
                    if end_dt.tzinfo is None or end_dt.tzinfo.utcoffset(end_dt) is None:
                        end_dt = pytz.utc.localize(end_dt)
                        end_dt_utc = end_dt.astimezone(pytz.utc)

                summary = str(component.get('summary'))
                if (start_dt > now) or (now < end_dt):
                    events.append({
                        'start': start_dt,
                        'end': end_dt,
                        'summary': summary
                        })
        if not events:
            print("No upcoming events found in calendar feed.")
            return

        events.sort(key=lambda x: x['start'])

        return events[:10]

    except requests.exceptions.HTTPError as e:
        print(f"Error fetching calendar data: HTTP {e.response.status_code}. Is the URL correct?")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")


def main():
    countdown = arsenal()
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


def arsenal():
    events = get_next_events()

    now = datetime.now(pytz.utc)

    if not events:
        print('No upcoming events found.')
        return "None Scheduled"
    for event in events:
        global summary
        summary = event['summary']
        start = event['start']
        end = event['end']
        if now >= start:
            return "Now!"
        time_remaining = start - now
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        print(f"Next event:\n{start} {summary}")
        print(f"Remaining: {days} days, {hours} hours, and {minutes} minutes.")
        return f'{days} days {hours} hours {minutes} minutes'

if __name__ == '__main__':
    main()
