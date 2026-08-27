#!/usr/bin/python3
"""
' Andrew Reifman-Packett
' May 2017
"""

import re
from pathlib import Path

from onebag import get_timestamp, login_bot

from sidebar.results.findMatches import build_table

REPO_ROOT = Path(__file__).resolve().parents[2]


def buildSidebar():
    body = "[//]: # (Fixtures Table)\n"
    body += "| Date | Result/Time | Opponent | [](#icon-trophy) |\n"
    body += "|:----:|:----:|:----:|:----:|\n"
    body += build_table()
    body += "[//]: # (End Fixtures Table)"
    return body


def updateResults():
    results = buildSidebar()
    r, subreddit = login_bot(str(REPO_ROOT))
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings["description"]
    contents = re.sub(
        "\[\/\/\]: # \(Fixtures Table\).*\[\/\/\]: # \(End Fixtures Table\)",
        results,
        contents,
        flags=re.DOTALL,
    )
    # r.subreddit(subreddit).mod.update(description=contents)
    r.subreddit(subreddit).wiki["config/sidebar"].edit(contents)


updateResults()
print(get_timestamp() + "Fixtures & Results Table Updated")
