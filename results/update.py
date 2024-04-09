#!/usr/bin/python3
'''
' Andrew Reifman-Packett
' May 2017
'''
import findMatches
import praw
import datetime
import re
from time import sleep


def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(
        datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(
        datetime.datetime.now().minute)
    t = '[' + hr + ':' + minute + '] '
    return dt + t


def loginBot():
    try:
        f = open('../login.txt')
        subreddit, user_agent, client_id, secret, refresh = f.readline().split('||', 5)
        f.close()
        r = praw.Reddit(client_id=client_id,
                        client_secret=secret,
                        refresh_token=refresh.strip(),
                        user_agent=user_agent)

        print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
    except Exception as e:
        print(getTimestamp() + str(e))
        print(getTimestamp() + "Setup error in Results \n")
        sleep(1)
        exit()

    return r, subreddit


def buildSidebar():
    body = "[//]: # (Fixtures Table)\n"
    body += "| Date | Result/Time | Opponent | [](#icon-trophy) |\n"
    body += "|:----:|:----:|:----:|:----:|\n"
    body += findMatches.main()
    body += "[//]: # (End Fixtures Table)"
    return body


def updateResults():
    results = buildSidebar()
    r, subreddit = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Fixtures Table\).*\[\/\/\]: # \(End Fixtures Table\)', results, contents,
                      flags=re.DOTALL)
    # r.subreddit(subreddit).mod.update(description=contents)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)


updateResults()
print(getTimestamp() + "Fixtures & Results Table Updated")
