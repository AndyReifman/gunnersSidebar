#!/usr/bin/python
# -*- coding: utf-8 -*-


import re,logging,logging.handlers,datetime,requests,requests.auth,sys,json,unicodedata
from praw.models import Message
from collections import Counter
from itertools import groupby
from time import sleep
from bs4 import BeautifulSoup


def getTimestamp():
        dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
        hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
        t = '[' + hr + ':' + min + '] '
        return dt + t
 
def getSprite(teamName):
    return {
         "AFC Bournemouth": "(#sprite1-p218)",
         "Arsenal": "(#sprite1-p1)",
         "Aston Villa": "(#sprite1-p19)",
         "Brighton & Hove Albion":"(#sprite1-p103)",
         "Burnley": "(#sprite1-p156)",
         "Cardiff City": "(#sprite1-p80)",
         "Chelsea": "(#sprite1-p4)",
         "Crystal Palace": "(#sprite1-p67)",
         "Everton": "(#sprite1-p15)",
         "Fulham": "(#sprite1-p29)",
         "Huddersfield Town":"(#sprite1-p199)",
         "Hull City": "(#sprite1-p117)",
         "Leicester City": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Manchester City": "(#sprite1-p10)",
         "Manchester United": "(#sprite1-p2)",
         "Newcastle United": "(#sprite1-p11)",
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


def getSign(goalDiff):
    if int(goalDiff) > 0:
        return "+"+goalDiff
    return goalDiff

def teamsAbove(table, index, i):
    body = ""
    if index < 0:
        return body
    elif index == 0:
        cells = table[1].findAll("td")
        position = cells[0].getText()
        team = cells[2].getText().strip().splitlines()[1]
        goalDiff = cells[19].getText()
        points = cells[20].getText()
        body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    else:
        for x in range(index, i):
            cells = table[x].findAll("td")
            position = cells[0].getText()
            team = cells[2].getText().strip().splitlines()[1]
            goalDiff = cells[19].getText()
            points = cells[20].getText()
            body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body

        
def teamsBelow(table, index,i):
    body = ""
    if index < 5:
        index = 5
    for x in range(i+1, index+1):
        cells = table[x].findAll("td")
        position = cells[0].getText()
        team = cells[2].getText().strip().splitlines()[1]
        goalDiff = cells[19].getText()
        points = cells[20].getText()
        body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body
    

def findArsenal(table):
    for index,row in enumerate(table):
        cells = row.findAll("td")
        position = cells[0].getText()
        team = cells[2].getText().strip().splitlines()[1]
        goalDiff = cells[19].getText()
        points = cells[20].getText()
        if team == "Arsenal":
            i = index
            body = "|**"+position+"**|[]"+getSprite(team)+"|**"+getSign(goalDiff)+"**|**"+points+"**|\n"
    topRange = i + 2
    botRange = i - 2
    if botRange <= 1:
        topRange += 1
    above = teamsAbove(table, botRange, i)
    below = teamsBelow(table, topRange, i)
    body = above + body + below
    return body


def parseWebsite():
    website = "https://www.arsenal.com/men/tables"
    tableWebsite = requests.get(website, timeout=15)
    table_html = tableWebsite.text
    soup = BeautifulSoup(table_html, "lxml")
    rows = soup.find("tbody").findAll("tr")
    return rows


def main():
    table = parseWebsite()
    body = findArsenal(table)
    return body
