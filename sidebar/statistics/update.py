#!/usr/bin/python3
"""
' Andrew Reifman-Packett
' May 2017
"""

import os
import re

from onebag import get_timestamp, login_bot

from sidebar.statistics.getAssists import get_assists
from sidebar.statistics.getGoals import get_goals


def buildGoalSidebar():
    body = "[//]: # (Goals Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += get_goals()
    body += "[//]: # (End Goals Table)"
    return body


def buildAssistsSidebar():
    body = "[//]: # (Assists Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += get_assists()
    body += "[//]: # (End Assists Table)"
    return body


def updateGoals():
    goals = buildGoalSidebar()
    assists = buildAssistsSidebar()
    r, subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings["description"]
    contents = re.sub(
        "\[\/\/\]: # \(Goals Table\).*\[\/\/\]: # \(End Goals Table\)",
        goals,
        contents,
        flags=re.DOTALL,
    )
    contents = re.sub(
        "\[\/\/\]: # \(Assists Table\).*\[\/\/\]: # \(End Assists Table\)",
        assists,
        contents,
        flags=re.DOTALL,
    )
    r.subreddit(subreddit).wiki["config/sidebar"].edit(contents)


updateGoals()
print(get_timestamp() + "Goals Table Updated")
print(get_timestamp() + "Assists Table Updated")
