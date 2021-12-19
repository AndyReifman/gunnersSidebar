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
         "Brentford":"(#sprite1-p198)",
         "Brighton and Hove Albion" : "(#sprite1-p103)",
         "Brighton & Hove Albion":"(#sprite1-p103)",
         "Brighton":"(#sprite1-p103)",
         "Burnley": "(#sprite1-p156)",
         "Cardiff City": "(#sprite1-p80)",
         "Chelsea": "(#sprite1-p4)",
         "Crystal Palace": "(#sprite1-p67)",
         "Everton": "(#sprite1-p15)",
         "Fulham": "(#sprite1-p29)",
         "Huddersfield Town":"(#sprite1-p199)",
         "Hull City": "(#sprite1-p117)",
         "Leeds United": "(#sprite1-p27)",
         "Leicester City": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Manchester City": "(#sprite1-p10)",
         "Manchester United": "(#sprite1-p2)",
         "Newcastle United": "(#sprite1-p11)",
         "Norwich City": "(#sprite1-p44)",
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
        cells = table[0].findAll("td")
        position = table[0].find("span",{"class","value"}).text
        team = table[0].find("span",{"class","long"}).text
        goalDiff = cells[9].text.strip()
        points = table[0].find("td",{"class","points"}).text
        body += "|**"+position+"**|[]"+getSprite(team)+"|"+goalDiff+"|"+points+"|\n"
    else:
        for x in range(index, i,2):
            cells = table[x].findAll("td")
            position = table[x].find("span",{"class","value"}).text
            team = table[x].find("span",{"class","long"}).text
            goalDiff = cells[9].text.strip()
            points = table[x].find("td",{"class","points"}).text
            body += "|**"+position+"**|[]"+getSprite(team)+"|"+goalDiff+"|"+points+"|\n"
    return body

def teamsBelow(table, index,i):
    body = ""
    if index < 10:
        index = 10
    for x in range(i+2, index+2,2):
        cells = table[x].findAll("td")
        position = table[x].find("span",{"class","value"}).text
        team = table[x].find("span",{"class","long"}).text
        goalDiff = cells[9].text.strip()
        points = table[x].find("td",{"class","points"}).text
        body += "|**"+position+"**|[]"+getSprite(team)+"|"+goalDiff+"|"+points+"|\n"
        #Needed in case Arsenal are in 19th
        if x >= 38:
            return body
    return body
    

def findArsenal(table):
    for index,row in enumerate(table):
        if index % 2 == 1:
            continue
        cells = row.findAll("td")
        position = row.find("span",{"class","value"}).text
        team = row.find("span",{"class","long"}).text
        goalDiff = cells[9].text.strip()
        points = row.find("td",{"class","points"}).text
        if team == "Arsenal":
            i = index
            body = "|**"+position+"**|[]"+getSprite(team)+"|**"+goalDiff+"**|**"+points+"**|\n"
            break
    topRange = i + 4
    botRange = i - 4
    if botRange < 0:
        topRange += 2
    above = teamsAbove(table, botRange, i)
    below = teamsBelow(table, topRange, i)
    body = above + body + below
    return body


def parseWebsite():
    website = "https://www.premierleague.com/tables"
    tableWebsite = requests.get(website, timeout=15)
    table_html = tableWebsite.text
    soup = BeautifulSoup(table_html, "lxml")
    rows = soup.find("tbody").findAll("tr")
    return rows


def main():
    table = parseWebsite()
    body = findArsenal(table)
    return body

if __name__== "__main__":
    main()
