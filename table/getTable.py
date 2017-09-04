#!/usr/bin/python
# -*- coding: utf-8 -*-


import re,logging,logging.handlers,datetime,requests,requests.auth,sys,json,unicodedata
from praw.models import Message
from collections import Counter
from itertools import groupby
from time import sleep

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
         "Brighton & Hove Albion":"(#sprite1-p103)",
         "Burnley": "(#sprite1-p156)",
         "Chelsea": "(#sprite1-p4)",
         "Crystal Palace": "(#sprite1-p67)",
         "Everton": "(#sprite1-p15)",
         "Huddersfield Town":"(#sprite1-p199)",
         "Hull City": "(#sprite1-p117)",
         "Leicester City": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Manchester City": "(#sprite1-p10)",
         "Manchester United": "(#sprite1-p2)",
         "Newcastle United": "(#sprite1-p11)",
         "Middlesbrough": "(#sprite1-p91)",
         "Southampton": "(#sprite1-p38)",
         "Stoke City": "(#sprite1-p81)",
         "Sunderland": "(#sprite1-p46)",
         "Swansea City": "(#sprite1-p39)",
         "Tottenham Hotspur": "(#icon-poop)",
         "Watford": "(#sprite1-p112)",
         "West Bromwich Albion": "(#sprite1-p78)",
         "West Ham United": "(#sprite1-p21)",
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
        team = re.findall('a href=".*">(.*)<\/a>',table[1])[0]
        position = re.findall('<td class="pos">(.*)</td>',table[1])[0]
        goalDiff = re.findall('<td class="gd">(.*)</td>',table[1])[0]
        points = re.findall('<td class="pts">(.*)</td>',table[1])[0]
        body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    else:
        for x in range(index, i):
            team = re.findall('a href=".*">(.*)<\/a>',table[x])[0]
            position = re.findall('<td class="pos">(.*)</td>',table[x])[0]
            goalDiff = re.findall('<td class="gd">(.*)</td>',table[x])[0]
            points = re.findall('<td class="pts">(.*)</td>',table[x])[0]
            body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body

def discordAbove(table, index, i):
    body = ""
    if index < 0:
        return body
    elif index == 0:
        team = re.findall('a href=".*">(.*)<\/a>',table[1])[0]
        position = re.findall('<td class="pos">(.*)</td>',table[1])[0]
        goalDiff = re.findall('<td class="gd">(.*)</td>',table[1])[0]
        points = re.findall('<td class="pts">(.*)</td>',table[1])[0]
        body += "|**"+position+"**|"+team+"|"+getSign(goalDiff)+"|"+points+"|\n"
    else:
        for x in range(index, i):
            team = re.findall('a href=".*">(.*)<\/a>',table[x])[0]
            position = re.findall('<td class="pos">(.*)</td>',table[x])[0]
            goalDiff = re.findall('<td class="gd">(.*)</td>',table[x])[0]
            points = re.findall('<td class="pts">(.*)</td>',table[x])[0]
            body += "|**"+position+"**|"+team+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body
        
def teamsBelow(table, index,i):
    body = ""
    if index < 5:
        index = 5
    for x in range(i+1, index+1):
            team = re.findall('a href=".*">(.*)<\/a>',table[x])[0]
            position = re.findall('<td class="pos">(.*)</td>',table[x])[0]
            goalDiff = re.findall('<td class="gd">(.*)</td>',table[x])[0]
            points = re.findall('<td class="pts">(.*)</td>',table[x])[0]
            body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body
    

def discordBelow(table, index,i):
    body = ""
    if index < 5:
        index = 5
    for x in range(i+1, index+1):
            team = re.findall('a href=".*">(.*)<\/a>',table[x])[0]
            position = re.findall('<td class="pos">(.*)</td>',table[x])[0]
            goalDiff = re.findall('<td class="gd">(.*)</td>',table[x])[0]
            points = re.findall('<td class="pts">(.*)</td>',table[x])[0]
            body += "|**"+position+"**|"+team+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body

def findArsenal(table):
    for index,pos in enumerate(table):
        team = re.findall('a href=".*">(.*)<\/a>',pos)[0]
        if team == "Arsenal":
            i = index
            position = re.findall('<td class="pos">(.*)</td>',pos)[0]
            goalDiff = re.findall('<td class="gd">(.*)</td>',pos)[0]
            points = re.findall('<td class="pts">(.*)</td>',pos)[0]
            body = "|**"+position+"**|[]"+getSprite(team)+"|**"+getSign(goalDiff)+"**|**"+points+"**|\n"
    topRange = i + 2
    botRange = i - 2
    if botRange <= 1:
        topRange += 1
    above = teamsAbove(table, botRange, i)
    below = teamsBelow(table, topRange, i)
    body = above + body + below
    return body

def discordBuild(table):
    for index,pos in enumerate(table):
        team = re.findall('a href=".*">(.*)<\/a>',pos)[0]
        if team == "Arsenal":
            i = index
            position = re.findall('<td class="pos">(.*)</td>',pos)[0]
            goalDiff = re.findall('<td class="gd">(.*)</td>',pos)[0]
            points = re.findall('<td class="pts">(.*)</td>',pos)[0]
            body = "|**"+position+"**|**"+team+"**|**"+getSign(goalDiff)+"**|**"+points+"**|\n"
    topRange = i + 2
    botRange = i - 2
    if botRange <= 1:
        topRange += 1
    above = discordAbove(table, botRange, i)
    below = discordBelow(table, topRange, i)
    body = above + body + below
    return body


def parseWebsite():
    website = "http://www.espnfc.us/english-premier-league/23/table"
    tableWebsite = requests.get(website, timeout=15)
    table_html = tableWebsite.text
    fullTable = table_html.split('<div class="responsive-table">')[1]
    table = fullTable.split('<tr style="background-color:')
    #fixtures[0] now holds the next match
    return table

def main():
    table = parseWebsite()
    body = findArsenal(table)
    #return body
    return body

def discordMain():
    table = parseWebsite()
    body = discordBuild(table)
    return body
