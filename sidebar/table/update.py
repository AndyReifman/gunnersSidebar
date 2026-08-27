#!/usr/bin/python3
import re
from pathlib import Path

from onebag import get_timestamp, login_bot

from sidebar.table.getTable import build_prem_table
from sidebar.table.uefaTable import build_uefa_table

REPO_ROOT = Path(__file__).resolve().parents[2]


def buildSidebar():
    body = "[//]: # (Premier Table)\n"
    body += "|\\#| Team | GD | Points \n"
    body += "|::|:-:|:--:|:--:|\n"
    body += build_prem_table()
    body += "[//]: # (End Premier Table)"
    return body


def build_uefa():
    body = "[//]: # (UEFA Table)\n"
    body += "|\\#| Team | GD | Points \n"
    body += "|::|:-:|:--:|:--:|\n"
    body += build_uefa_table()
    body += "[//]: # (End UEFA Table)"
    return body


# Update the sidebar
def updateSidebar():
    eplTable = buildSidebar()
    uefa = build_uefa()
    r, subreddit = login_bot(str(REPO_ROOT))
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings["description"]
    # We want to update current sidebar to where injury table goes
    contents = re.sub(
        "\[\/\/\]: # \(Premier Table\).*\[\/\/\]: # \(End Premier Table\)",
        eplTable,
        contents,
        flags=re.DOTALL,
    )
    contents = re.sub(
        "\[\/\/\]: # \(UEFA Table\).*\[\/\/\]: # \(End UEFA Table\)",
        uefa,
        contents,
        flags=re.DOTALL,
    )
    r.subreddit(subreddit).wiki["config/sidebar"].edit(contents)
    print(get_timestamp() + "Premier League Table Updated")


updateSidebar()
