#!/usr/bin/python3
"""
' Andrew Reifman-Packett
' May 2017
"""

import findMatches
import re

from helpers import getTimestamp, loginBot


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
