#!/usr/bin/python3
"""
' Andrew Reifman-Packett
' May 2017
"""
import os

from onebag import login_bot, get_timestamp

import findMatches
import re


def buildSidebar():
    body = "[//]: # (Fixtures Table)\n"
    body += "| Date | Result/Time | Opponent | [](#icon-trophy) |\n"
    body += "|:----:|:----:|:----:|:----:|\n"
    body += findMatches.main()
    body += "[//]: # (End Fixtures Table)"
    return body


def updateResults():
    results = buildSidebar()
    r, subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Fixtures Table\).*\[\/\/\]: # \(End Fixtures Table\)', results, contents,
                      flags=re.DOTALL)
    # r.subreddit(subreddit).mod.update(description=contents)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)


updateResults()
print(get_timestamp() + "Fixtures & Results Table Updated")
