#!/usr/bin/python
# -*- coding: utf-8 -*-

import praw,re,logging,logging.handlers,datetime,requests,requests.auth,sys,json,unicodedata
from praw.models import Message
from collections import Counter
from itertools import groupby
from time import sleep

i = 0

class Match(object):
    date = ""
    homeTeam = ""
    awayTeam = ""
    timeResult = ""
    comp = ""

    def __init__(self,date,homeTeam,awayTeam,timeResult,comp):
        self.date = date
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.timeResult = timeResult
        self.comp = comp

def getTimestamp():
        dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
        hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
        t = '[' + hr + ':' + min + '] '
        return dt + t

def getLocation(line):
    homeTeam = line[0]
    if homeTeam == 'Arsenal':
        return 0
    else:
        return 1

def getSprite(teamName):
    return {
         "Arsenal": "(#sprite1-p1)",
         "Bournemouth": "(#sprite1-p218)",
         "BATE":"(#sprite4-43)",
         "Burnley": "(#sprite1-p156)",
         "Chelsea": "(#sprite1-p4)",
         "Cologne":"(#sprite1-p125)",
         "Crystal Palace": "(#sprite1-p67)",
         "Doncaster": "(#sprite1-p252)",
         "Everton": "(#sprite1-p15)",
         "Hull City": "(#sprite1-p117)",
         "Leicester": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Manchester City": "(#sprite1-p10)",
         "Manchester United": "(#sprite1-p2)",
         "Middlesbrough": "(#sprite1-p91)",
         "Red Star Bel":"(#sprite1-165)",
         "Sevilla": "(#sprite1-p229)",
         "Southampton": "(#sprite1-p38)",
         "Stoke": "(#sprite1-p81)",
         "Sunderland": "(#sprite1-p46)",
         "Swansea City": "(#sprite1-p39)",
         "Tottenham Hotspur": "(#icon-poop)",
         "Watford": "(#sprite1-p112)",
         "West Bromwich Albion": "(#sprite1-p78)",
         "West Ham United": "(#sprite1-p21)",
        }[teamName]

def getComp(comp):
    return {
        "CC":"(#logo-eflcup)",
        "Emirates Cup":"(#icon-ball)",
        "Europa League":"(#logo-el)",
        "FA Community Shield":"(#logo-communityshield)",
        "Premier League":"(#logo-pl)",
      }[comp]

def parseWebsite():
    website = "http://www.espnfc.us/club/arsenal/359/fixtures"
    fixturesWebsite = requests.get(website, timeout=15)
    fixture_html = fixturesWebsite.text
    nextMatch = fixture_html.split('<div class="score-column score-date">')[1]
    games = fixture_html.split('<div class="games-container">')[1]
    fixtures = games.split('<div class="score-column score-date">')[1:]
    #fixtures[0] now holds the next match
    return nextMatch,fixtures

def findNext(fixtures, nextMatch):
    for index,fixture in enumerate(fixtures):
        date = re.findall('div class="date">(.*)<\/div>',fixture)[0] 
        if date == nextMatch.date:
            i = index
    results = findResults(fixtures, i)
    matches = findMatches(fixtures, i)
    body = results + matches
    return body

def discordNext(fixtures, nextMatch):
    for index,fixture in enumerate(fixtures):
        date = re.findall('div class="date">(.*)<\/div>',fixture)[0] 
        if date == nextMatch.date:
            i = index
    matches = discordMatches(fixtures, i)
    body = matches
    return body

def discordBefore(fixtures, nextMatch):
    for index,fixture in enumerate(fixtures):
        date = re.findall('div class="date">(.*)<\/div>',fixture)[0] 
        if date == nextMatch.date:
            i = index
    results = discordResults(fixtures, i)
    body = results
    return body

def discordMatches(fixtures, index):
    body = ""
    team = ""
    x = index + 3
    for s in range(index, x):
        date = re.findall('div class="date">(.*)<\/div>',fixtures[s])[0]
        date = date.split(',')[0]
        time = re.findall('<div class="time gmt-time" data-time="(.*)">',fixtures[s])[0]
        time = re.findall('.*T(.*):',time)[0]
        comp = re.findall('<div class="league">(.*)<\/div>',fixtures[s])[0]
        teams = re.findall('<div class="team-name.*">(.*)<\/div>',fixtures[s])
        homeTeam = teams[0]
        awayTeam = teams[1]
        homeAway = getLocation(teams)
        if homeAway == 0:
            team = awayTeam + " (H)"
        else:
            team = homeTeam + " (A)"
        body += "| " + date + " |  " + time + " | " + team +" | " +comp+" |\n"
    return body

def discordResults(fixtures,index):
    body = ""
    team = ""
    x = index - 3
    for s in range(x, index): 
        result = ""
        date = re.findall('div class="date">(.*)<\/div>',fixtures[s])[0]
        date = date.split(',')[0]
        comp = re.findall('<div class="league">(.*)<\/div>',fixtures[s])[0]
        teams = re.findall('<div class="team-name.*">(.*)<\/div>',fixtures[s])
        homeTeam = teams[0]
        awayTeam = teams[1]
        if re.findall('<div class="status">(.*)<\/div>',fixtures[s])[0] == "FT-Pens":
            homeScore = re.findall('<span class="home-score score-value.*">(.*)<',fixtures[s])[0]
            homePenScore = re.findall('\(([0-9])\)',homeScore)[0]
            homeScore = re.findall('\s+([0-9])',homeScore)[0]
            awayScore = re.findall('<span class="away-score score-value.*">(.*)<',fixtures[s])[0]
            awayPenScore = re.findall('\(([0-9])\)',awayScore)[0]
            awayScore = re.findall('([0-9])\s+',awayScore)[0]
            homeAway = getLocation(teams)
            #0 for home, 1 for away
            homeAway = getLocation(teams)
            if homePenScore > awayPenScore:
                if homeAway == 0:
                    result += "win) "
                else:
                    result += "loss) "
            elif homePenScore < awayPenScore: 
                if homeAway == 0:
                    result += "loss) "
                else:
                    result += "win) "
            result += homeScore + " ("+homePenScore+") - ("+awayPenScore+") "+awayScore
            if homeAway == 0:
                team = awayTeam + " (H)"
            else:
                team = homeTeam + " (A)"
        else:
            homeScore = re.findall('<span class="home-score score-value.*">(.*)<',fixtures[s])[0]
            awayScore = re.findall('<span class="away-score score-value.*">(.*)<',fixtures[s])[0]
            homeAway = getLocation(teams)
            #0 for home, 1 for away
            homeAway = getLocation(teams)
            if homeScore > awayScore:
                if homeAway == 0:
                    result += "win "
                else:
                    result += "loss "
            elif homeScore < awayScore: 
                if homeAway == 0:
                    result += "loss "
                else:
                    result += "win "
            else:
                result += "draw "
            result += homeScore +" - "+awayScore
            if homeAway == 0:
                team = awayTeam + " (H)"
            else:
                team = homeTeam + " (A)"
        body += "| " + date + " | " + result + " | " + team +" | " +comp+"|\n"
    return body


def findResults(fixtures, index):
    body = ""
    team = ""
    x = index - 3
    for s in range(x, index): 
        result = ""
        date = re.findall('div class="date">(.*)<\/div>',fixtures[s])[0]
        date = date.split(',')[0]
        comp = re.findall('<div class="league">(.*)<\/div>',fixtures[s])[0]
        teams = re.findall('<div class="team-name.*">(.*)<\/div>',fixtures[s])
        homeTeam = teams[0]
        awayTeam = teams[1]
        if re.findall('<div class="status">(.*)<\/div>',fixtures[s])[0] == "FT-Pens":
            homeScore = re.findall('<span class="home-score score-value.*">(.*)<',fixtures[s])[0]
            homePenScore = re.findall('\(([0-9])\)',homeScore)[0]
            homeScore = re.findall('\s+([0-9])',homeScore)[0]
            awayScore = re.findall('<span class="away-score score-value.*">(.*)<',fixtures[s])[0]
            awayPenScore = re.findall('\(([0-9])\)',awayScore)[0]
            awayScore = re.findall('([0-9])\s+',awayScore)[0]
            homeAway = getLocation(teams)
            #0 for home, 1 for away
            homeAway = getLocation(teams)
            if homePenScore > awayPenScore:
                if homeAway == 0:
                    result += "[](#icon-win) "
                else:
                    result += "[](#icon-loss) "
            elif homePenScore < awayPenScore: 
                if homeAway == 0:
                    result += "[](#icon-loss) "
                else:
                    result += "[](#icon-win) "
            result += homeScore + " ("+homePenScore+") - ("+awayPenScore+") "+awayScore
            if homeAway == 0:
                team = getSprite(awayTeam) + " (H)"
            else:
                team = getSprite(homeTeam) + " (A)"
        else:
            homeScore = re.findall('<span class="home-score score-value.*">(.*)<',fixtures[s])[0]
            awayScore = re.findall('<span class="away-score score-value.*">(.*)<',fixtures[s])[0]
            homeAway = getLocation(teams)
            #0 for home, 1 for away
            homeAway = getLocation(teams)
            if homeScore > awayScore:
                if homeAway == 0:
                    result += "[](#icon-win) "
                else:
                    result += "[](#icon-loss) "
            elif homeScore < awayScore: 
                if homeAway == 0:
                    result += "[](#icon-loss) "
                else:
                    result += "[](#icon-win) "
            else:
                result += "[](#icon-draw) "
            result += homeScore +" - "+awayScore
            if homeAway == 0:
                team = getSprite(awayTeam) + " (H)"
            else:
                team = getSprite(homeTeam) + " (A)"
        body += "| " + date + " | " + result + " | []" + team +" | []" +getComp(comp)+"|\n"
    body+="|||\n"
    return body

 
def findMatches(fixtures, index):
    body = ""
    team = ""
    x = index + 3
    for s in range(index, x):
        date = re.findall('div class="date">(.*)<\/div>',fixtures[s])[0]
        date = date.split(',')[0]
        time = re.findall('<div class="time gmt-time" data-time="(.*)">',fixtures[s])[0]
        time = re.findall('.*T(.*):',time)[0]
        comp = re.findall('<div class="league">(.*)<\/div>',fixtures[s])[0]
        teams = re.findall('<div class="team-name.*">(.*)<\/div>',fixtures[s])
        homeTeam = teams[0]
        awayTeam = teams[1]
        homeAway = getLocation(teams)
        if homeAway == 0:
            team = getSprite(awayTeam) + " (H)"
        else:
            team = getSprite(homeTeam)+ " (A)"
        body += "| " + date + " | [](#icon-clock) " + time + " | []" + team +" | []" +getComp(comp)+"|\n"
    return body
         

def parseNext(nextFixture):
    date = re.findall('div class="date">(.*)<\/div>',nextFixture)[0]
    time = re.findall('<div class="time gmt-time" data-time="(.*)">',nextFixture)[0]
    time = re.findall('.*T(.*):',time)[0]
    comp = re.findall('<div class="league">(.*)<\/div>',nextFixture)[0]
    teams = re.findall('<div class="team-name">(.*)<\/div>',nextFixture)
    homeTeam = teams[0]
    awayTeam = teams[1]
    nextMatch = Match(date,homeTeam,awayTeam,time,comp)
    return nextMatch

def main():
    nextMatch,fixtures = parseWebsite()
    nextMatch = parseNext(nextMatch)   
    body = findNext(fixtures,nextMatch)
    return body

def discordFixtures():
    nextMatch,fixtures = parseWebsite()
    nextMatch = parseNext(nextMatch)   
    body = discordNext(fixtures,nextMatch)
    return body 

def discordResult():
    nextMatch,fixtures = parseWebsite()
    nextMatch = parseNext(nextMatch)   
    body = discordBefore(fixtures,nextMatch)
    return body 
