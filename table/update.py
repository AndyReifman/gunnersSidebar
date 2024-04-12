#!/usr/bin/python3
import getTable
import europaTable
import re


from helpers import getTimestamp, loginBot


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


# Update the sidebar
def updateSidebar():
    eplTable = buildSidebar()
    # europaTable = buildEuropa()
    r, subreddit = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    # We want to update current sidebar to where injury table goes
    contents = re.sub('\[\/\/\]: # \(Premier Table\).*\[\/\/\]: # \(End Premier Table\)', eplTable, contents,
                      flags=re.DOTALL)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)
    print(getTimestamp() + "Premier League Table Updated")


updateSidebar()
