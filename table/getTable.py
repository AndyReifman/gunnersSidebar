#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import requests.auth


def getSprite(teamName):
    return {
        "AFC Bournemouth": "(#sprite1-p218)",
        "Arsenal": "(#sprite1-p1)",
        "Aston Villa": "(#sprite1-p19)",
        "Bournemouth": "(#sprite1-p218)",
        "Brentford": "(#sprite1-p198)",
        "Brighton and Hove Albion": "(#sprite1-p103)",
        "Brighton & Hove Albion": "(#sprite1-p103)",
        "Brighton": "(#sprite1-p103)",
        "Burnley": "(#sprite1-p156)",
        "Cardiff City": "(#sprite1-p80)",
        "Chelsea": "(#sprite1-p4)",
        "Crystal Palace": "(#sprite1-p67)",
        "Everton": "(#sprite1-p15)",
        "Fulham": "(#sprite1-p29)",
        "Huddersfield Town": "(#sprite1-p199)",
        "Hull City": "(#sprite1-p117)",
        "Leeds United": "(#sprite1-p27)",
        "Leicester City": "(#sprite1-p87)",
        "Liverpool": "(#sprite1-p3)",
        "Manchester City": "(#sprite1-p10)",
        "Manchester United": "(#sprite1-p2)",
        "Newcastle United": "(#sprite1-p11)",
        "Norwich City": "(#sprite1-p44)",
        "Nottingham Forest": "(#sprite1-p66)",
        "Middlesbrough": "(#sprite1-p91)",
        "Sheffield United": "(#sprite1-p159)",
        "Southampton": "(#sprite1-p38)",
        "Stoke City": "(#sprite1-p81)",
        "Sunderland": "(#sprite1-p46)",
        "Swansea City": "(#sprite1-p39)",
        "Tottenham Hotspur": "(#icon-poop)",
        "Watford": "(#sprite1-p112)",
        "West Bromwich Albion": "(#sprite1-p78)",
        "West Ham United": "(#sprite1-p21)",
        "Wolverhampton Wanderers": "(#sprite1-p70)",
        "Wolves": "(#sprite1-p70)",
    }[teamName]


def get_sign(goalDiff):
    if int(goalDiff) > 0:
        return f"+{goalDiff}"
    return goalDiff

def build_row(row, arsenal=False):
    """
    Build row string given a json row
    :param row: The row containing all the details we want
    :param arsenal: If this row is for Arsenal, bold all fields
    :return: A string containing a row in the table
    """
    team = row.get('team').get('name')
    overall = row.get('overall')
    pos = overall.get('position')
    goal_diff = overall.get('goalsFor') - overall.get('goalsAgainst')
    points = overall.get('points')
    if arsenal:
        body = f"|**{pos}**|**[]{getSprite(team)}**|**{get_sign(goal_diff)}**|**{points}**|\n"
    else:
        body = f"|**{pos}**|[]{getSprite(team)}|{get_sign(goal_diff)}|{points}|\n"
    return body

def build_table(table):
    pos = next((i for i, d in enumerate(table) if d.get('team').get('name') == 'Arsenal'), -1)
    start = max(0, pos - 2)
    end = min(20, pos + 3)
    if end - start < 5:
        if start == 0:
            end = 5
        elif end == 20:
            start = 15
    table = list(enumerate(table))[start:end]
    body = ''.join(build_row(row, arsenal=(i == pos)) for i, row in table)
    return body


def parseWebsite():
    website = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v5/competitions/8/seasons/2025/standings?live=false"
    tableWebsite = requests.get(website, timeout=15)
    response_json = tableWebsite.json()
    table = response_json.get('tables')[0].get('entries')
    return table


def main():
    table = parseWebsite()
    body = build_table(table)
    return body


if __name__ == "__main__":
    print(main())
