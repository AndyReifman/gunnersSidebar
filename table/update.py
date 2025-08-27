#!/usr/bin/python3
import os

from onebag import login_bot, get_timestamp

import getTable
import europaTable
import re


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
    r, subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    # We want to update current sidebar to where injury table goes
    contents = re.sub('\[\/\/\]: # \(Premier Table\).*\[\/\/\]: # \(End Premier Table\)', eplTable, contents,
                      flags=re.DOTALL)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)
    print(get_timestamp() + "Premier League Table Updated")


updateSidebar()
