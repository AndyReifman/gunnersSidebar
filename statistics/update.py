#!/usr/bin/python3
"""
' Andrew Reifman-Packett
' May 2017
"""
import getGoals
import getAssists
import re

from helpers import getTimestamp, loginBot


def buildGoalSidebar():
    body = "[//]: # (Goals Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += getGoals.main()
    body += "[//]: # (End Goals Table)"
    return body


def buildAssistsSidebar():
    body = "[//]: # (Assists Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += getAssists.main()
    body += "[//]: # (End Assists Table)"
    return body


def updateGoals():
    goals = buildGoalSidebar()
    assists = buildAssistsSidebar()
    r, subreddit = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Goals Table\).*\[\/\/\]: # \(End Goals Table\)', goals, contents, flags=re.DOTALL)
    contents = re.sub('\[\/\/\]: # \(Assists Table\).*\[\/\/\]: # \(End Assists Table\)', assists, contents,
                      flags=re.DOTALL)
    r.subreddit(subreddit).wiki['config/sidebar'].edit(contents)


updateGoals()
print(getTimestamp() + "Goals Table Updated")
print(getTimestamp() + "Assists Table Updated")
