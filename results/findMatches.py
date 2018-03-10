#!/usr/bin/python
# -*- coding: utf-8 -*-

import praw,re,logging,logging.handlers,datetime,requests,requests.auth,sys,json,unicodedata
from unidecode import unidecode
from praw.models import Message
from collections import Counter
from itertools import groupby
from time import sleep
from bs4 import BeautifulSoup

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
    homeTeam = line[0].text
    if homeTeam == 'Arsenal':
        return 0
    else:
        return 1

def getSprite(teamName):
    return {
         "Arsenal": "(#sprite1-p1)",
         "Bournemouth": "(#sprite1-p218)",
         "BATE":"(#sprite4-p43)",
         "Brighton":"(#sprite1-p103)",
         "Burnley": "(#sprite1-p156)",
         "Chelsea": "(#sprite1-p4)",
         "Cologne":"(#sprite1-p125)",
         "C Palace": "(#sprite1-p67)",
         "Doncaster": "(#sprite1-p252)",
         "Everton": "(#sprite1-p15)",
         "Huddersfield": "(#sprite1-p199)",
         "Hull City": "(#sprite1-p117)",
         "Leicester": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Man City": "(#sprite1-p10)",
         "Man Utd": "(#sprite1-p2)",
         "Middlesbrough": "(#sprite1-p91)",
         "Milan": "(#sprite1-p13)",
         "Newcastle": "(#sprite1-p11)",
         "Norwich": "(#sprite1-p44)",
         "Nottm Forest": "(#sprite1-p66)",
         "Ostersunds F": "(#sprite2-p48)",
         "Red Star Bel":"(#sprite1-p165)",
         "Sevilla": "(#sprite1-p229)",
         "Southampton": "(#sprite1-p38)",
         "Stoke": "(#sprite1-p81)",
         "Sunderland": "(#sprite1-p46)",
         "Swansea": "(#sprite1-p39)",
         "Tottenham": "(#icon-poop)",
         "Watford": "(#sprite1-p112)",
         "West Brom": "(#sprite1-p78)",
         "West Ham": "(#sprite1-p21)",
        }[teamName]

def getComp(comp):
    return {
        "CC":"(#logo-eflcup)",
        "Emirates Cup":"(#icon-ball)",
        "English Carabao Cup":"(#logo-eflcup)",
        "Europa League":"(#logo-el)",
        "FA Community Shield":"(#logo-communityshield)",
        "Premier League":"(#logo-pl)",
        "English FA Cup":"(#logo-facup)",
      }[comp]

def parseWebsite():
    website = "http://www.espnfc.us/club/arsenal/359/fixtures"
    fixturesWebsite = requests.get(website, timeout=15)
    fixture_html = fixturesWebsite.text
    soup = BeautifulSoup(fixture_html, "lxml")
    nextMatch = soup.find("div",{"class","next-match-list games-container"})
    table = soup.findAll("div",{"class","games-container"})[1]
    #fixtures[0] now holds the next match
    return nextMatch,table

def findNext(table, nextMatch):
    fixtures = table.findAll("a")
    for index,fixture in enumerate(fixtures):
        date = fixture.find("div",{"class","date"}).text
        if date == nextMatch.date:
            i = index
    results = findResults(fixtures, i)
    matches = findMatches(fixtures, i)
    body = results + matches
    return body


def findResults(fixtures, index):
    body = ""
    team = ""
    x = index - 3
    for s in range(x, index): 
        result = ""
	date = fixtures[s].find("div",{"class","date"}).text
        date = date.split(',')[0]
	comp = fixtures[s].find("div",{"class","league"}).text
	teams = fixtures[s].findAll("div",{"class","team-name"})
        homeTeam = unidecode(teams[0].text)
        awayTeam = unidecode(teams[1].text)
	if fixtures[s].find("div",{"class","status"}).text == "FT-Pens":
            homeScore = fixtures[s].find("span",{"class",re.compile(r'home-score score-value')})[0].text
            homePenScore = re.findall('\(([0-9])\)',homeScore)[0]
            homeScore = re.findall('\s+([0-9])',homeScore)[0]
	    awayScore = fixtures[s].findAll("span",{"class",re.compile(r'away-score score-value')})[0].text
            awayPenScore = re.findall('\(([0-9])\)',awayScore)[0]
            awayScore = re.findall('([0-9])\s+',awayScore)[0]
            homeAway = getLocation(teams)
            #0 for home, 1 for away
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
            homeScore = fixtures[s].findAll("span",{"class",re.compile(r'home-score score-value')})[0].text
	    awayScore = fixtures[s].findAll("span",{"class",re.compile(r'away-score score-value')})[0].text
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
    s = index
    while s < x:
	date = fixtures[s].find("div",{"class","date"}).text
        date = date.split(',')[0]
	time = fixtures[s].find("div",{"class","time"}).text
	print time
	if time == "TBD":
	    x += 1
	    s += 1
	    continue
        time = re.search('.*T(.*):',fixtures[s].find("div",{"class","time"})['data-time']).group(1)
	print time
	comp = fixtures[s].find("div",{"class","league"}).text
	teams = fixtures[s].findAll("div",{"class","team-name"})
        homeTeam = unidecode(teams[0].text)
        awayTeam = unidecode(teams[1].text)
        homeAway = getLocation(teams)
        if homeAway == 0:
            team = getSprite(awayTeam) + " (H)"
        else:
            team = getSprite(homeTeam)+ " (A)"
        body += "| " + date + " | [](#icon-clock) " + time + " | []" + team +" | []" +getComp(comp)+"|\n"
	s += 1
    return body
         

def parseNext(nextFixture):
    #date = nextFixture.find("span",{"class","time"})['data-time'].split("T")[0]
    date = nextFixture.find("div",{"class","date"}).text
    time = re.search('.*T(.*)\.',nextFixture.find("div",{"class","time"})['data-time']).group(1)
    comp = nextFixture.find("div",{"class","league"}).text
    teams = nextFixture.findAll("div",{"class","team-name"})
    homeTeam = teams[0].text
    awayTeam = teams[1].text
    nextMatch = Match(date,homeTeam,awayTeam,time,comp)
    return nextMatch

def main():
    nextMatch,table = parseWebsite()
    nextMatch = parseNext(nextMatch)
    body = findNext(table,nextMatch)
    return body

