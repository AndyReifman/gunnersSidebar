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
    homeTeam = line[0].text.strip()
    if 'Arsenal' in homeTeam:
        return 0
    else:
        return 1

def getSprite(teamName):
    return {
         "AC Milan": "(#sprite1-p13)",
         "Arsenal": "(#sprite1-p1)",
         "Bournemouth": "(#sprite1-p218)",
         "BATE":"(#sprite4-p43)",
         "Brighton & Hove Albion":"(#sprite1-p103)",
         "Burnley": "(#sprite1-p156)",
         "C Palace": "(#sprite1-p67)",
         "Chelsea": "(#sprite1-p4)",
         "Cologne":"(#sprite1-p125)",
         "CSKA Moscow":"(#sprite1-p220)",
         "Doncaster": "(#sprite1-p252)",
         "Everton": "(#sprite1-p15)",
         "Huddersfield": "(#sprite1-p199)",
         "Hull City": "(#sprite1-p117)",
         "Leicester": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Man City": "(#sprite1-p10)",
         "Man Utd": "(#sprite1-p2)",
         "Middlesbrough": "(#sprite1-p91)",
         "Newcastle United": "(#sprite1-p11)",
         "Norwich": "(#sprite1-p44)",
         "Nottm Forest": "(#sprite1-p66)",
         "Ostersunds F": "(#sprite2-p48)",
         "Red Star Bel":"(#sprite1-p165)",
         "Sevilla": "(#sprite1-p229)",
         "Southampton": "(#sprite1-p38)",
         "Stoke City": "(#sprite1-p81)",
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

def parseFixtures():
    website = "https://www.arsenal.com/fixtures"
    fixtureWebsite = requests.get(website,timeout=15)
    fixture_html = fixtureWebsite.text
    soup = BeautifulSoup(fixture_html, "lxml")
    table = soup.find("div",{"class","accordions"})
    matches = table.findAll("article",attrs={'role':'article'})
    return matches

def parseResults():
    website = "https://www.arsenal.com/results"
    fixtureWebsite = requests.get(website,timeout=15)
    fixture_html = fixtureWebsite.text
    soup = BeautifulSoup(fixture_html, "lxml")
    table = soup.find("div",{"class","accordions"})
    matches = table.findAll("article",attrs={'role':'article'})
    return matches


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


def findFixtures(matches):
    body = ""
    match = matches[0].find("div",{"class","fixture-match"})
    date = matches[0].find("time").text
    time = date.split('-')[1].strip()
    date = date.split('-')[0][3:].strip()
    comp = matches[0].find("div",{"class","event-info__extra"}).text
    teams = match.findAll("div",{"class","fixture-match__team"})
    homeTeam = teams[0].find("div",{"class","team-crest__name-value"}).text
    awayTeam = teams[1].find("div",{"class","team-crest__name-value"}).text
    homeAway = getLocation(teams)
    if homeAway == 0:
        team = getSprite(awayTeam) + " (H)"
    else:
        team = getSprite(homeTeam) + " (A)"
    body += "| " + date + " | [](#icon-clock) " + time + " | []" + team +" | []" +getComp(comp)+"|\n"
    for i in range(1,3):
        match = matches[i].find("div",{"class","card__content"})
        try:
            date = matches[i].find("time").text
            time = date.split('-')[1].strip()
            date = date.split('-')[0][3:].strip()
            comp = matches[i].find("div",{"class","event-info__extra"}).text
        except:
            time = "TBD"
            date = matches[i].find("div",class_=False, id=False).text[3:].strip()
            comp = matches[i].find("div",{"class","event-info__extra"}).text
        team = match.find("span",{"class","team-crest__name-value"}).text
        location = match.find("div",{"class","location-icon"})['title']
        if location == "Home":
            team = getSprite(team) + " (H)"
        else:
            team = getSprite(team)+ " (A)"
        body += "| " + date + " | [](#icon-clock) " + time + " | []" + team + " | []" +getComp(comp)+"|\n"
    return body

def findResults(matches):
    body = ""
    for i in range(2,0,-1):
        result = ""
        match = matches[i].find("div",{"class","card__content"})
        date = matches[i].find("time").text
        date = date.split('-')[0][3:].strip()
        comp = matches[i].find("div",{"class","event-info__extra"}).text
        team = match.find("span",{"class","team-crest__name-value"}).text
        location = match.find("div",{"class","location-icon"})['title']
        homeScore = match.findAll("span",{"class","scores__score"})[0].text
        awayScore = match.findAll("span",{"class","scores__score"})[1].text
        if homeScore > awayScore:
            if location == "Home":
                result += "[](#icon-win) "
            else:
                result += "[](#icon-loss) "
        elif homeScore < awayScore: 
            if location == "Home":
                result += "[](#icon-loss) "
            else:
                result += "[](#icon-win) "
        else:
            result += "[](#icon-draw) "
        result += homeScore +" - "+awayScore
        if location == "Home":
            team = getSprite(team) + " (H)"
        else:
            team = getSprite(team)+ " (A)"
        body += "| " + date + " | " + result + " | []" + team + " | []" +getComp(comp)+"|\n"
    result = ""
    date = matches[0].find("time").text
    date = date.split('-')[0][3:].strip()
    match = matches[0].find("div",{"class","fixture-match"})
    comp = matches[0].find("div",{"class","event-info__extra"}).text
    teams = match.findAll("div",{"class","fixture-match__team"})
    homeTeam = teams[0].find("div",{"class","team-crest__name-value"}).text
    awayTeam = teams[1].find("div",{"class","team-crest__name-value"}).text
    homeAway = getLocation(teams)
    homeScore = match.findAll("span",{"class","scores__score"})[0].text
    awayScore = match.findAll("span",{"class","scores__score"})[1].text
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

    body +="|||\n"
    return body


def main():
    matches = parseFixtures()
    results = parseResults()
    body = findResults(results)
    body += findFixtures(matches)
#    body = findNext(table,nextMatch)
    return body

