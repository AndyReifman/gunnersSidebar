#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import requests.auth

def get_sprite(team):
    return {
        "Ajax": "(#sprite1-p22)",
        "Arsenal": "(#sprite1-p1)",
        "Atalanta": "(#sprite2-p182)",
        "Athletic Club": "(#sprite1-p171)",
        "Atleti": "(#sprite1-p76)",
        "B. Dortmund": "(#sprite1-p12)",
    }[team]

def get_sign(goal_diff):
    if goal_diff > 0:
        return f"+{goal_diff}"
    return goal_diff

def parse_website():
    website = "https://standings.uefa.com/v1/standings?competitionId=1&seasonYear=2026"
    response = requests.get(website, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
    table = response.json()[0].get('items')
    return table

def build_row(row, pos, arsenal=False):
    """
    Build row string given a json row
    :param row: The row containing all the details we want
    :param arsenal: If this row is for Arsenal, bold all fields
    :return: A string containing a row in the table
    """
    team = row.get('team').get('internationalName')
    # pos = row.get('rank') Commenting out until after MW 1 when it will hopefully fix
    goal_diff = row.get('goalDifference')
    points = row.get('points')
    if arsenal:
        body = f"|**{pos}**|**[]{get_sprite(team)}**|**{get_sign(goal_diff)}**|**{points}**|\n"
    else:
        body = f"|**{pos}**|[]{get_sprite(team)}|{get_sign(goal_diff)}|{points}|\n"
    return body

def build_table(table):
    body = ""
    pos = next((i for i, d in enumerate(table) if d.get('team').get('internationalName') == 'Arsenal'), -1)
    start = max(0, pos - 2)
    end = min(20, pos + 3)
    if end - start < 5:
        if start == 0:
            end = 5
        elif end == 34:
            start = 29
    table = list(enumerate(table))[start:end]
    body = ''.join(build_row(row, (i+1), arsenal=(i == pos)) for i, row in table)
    return body

def main():
    table = parse_website()
    body = build_table(table)
    return body

if __name__ == '__main__':
    print(main())