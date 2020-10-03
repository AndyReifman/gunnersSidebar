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
         "AFC Bournemouth": "(#sprite1-p218)",
         "Al-Nasr Dubai SC": "(#sprite4-p375",
         "Angers": "(#sprite4-p32)",
         "Arsenal": "(#sprite1-p1)",
         "Aston Villa": "(#sprite1-p19)",
         "Atletico Madrid": "(#sprite1-p76)",
         "Barcelona": "(#sprite1-p6)",
         "Barnet":"(#sprite1-p245)",
         "Bayern Munich": "(#sprite1-p8)",
         "Blackpool": "(#sprite1-p146)",
         "Blackpool FC": "(#sprite1-p146)",
         "Boreham Wood": "(#sprite4-p375)",
         "Bournemouth": "(#sprite1-p218)",
         "BATE":"(#sprite4-p43)",
         "BATE Borisov": "(#sprite4-p43)",
         "Brentford":"(#sprite1-p198)",
         "Brighton":"(#sprite1-p103)",
         "Brighton & Hove Albion":"(#sprite1-p103)",
         "Burnley": "(#sprite1-p156)",
         "Crystal Palace": "(#sprite1-p67)",
         "Cardiff City":"(#sprite1-p80)",
         "Chelsea": "(#sprite1-p4)",
         "Cologne":"(#sprite1-p125)",
         "Colorado Rapids":"(#sprite1-p93)",
         "CSKA Moscow":"(#sprite1-p220)",
         "Doncaster": "(#sprite1-p252)",
         "Everton": "(#sprite1-p15)",
         "FC Vorskla": "(#sprite4-p133)",
         "Final":"(#sprite1-p02)",
         "Fiorentina": "(#sprite1-p149)",
         "Frankfurt": "(#sprite1-p86)",
         "Fulham": "(#sprite1-p29)",
         "Huddersfield Town": "(#sprite1-p199)",
         "Hull City": "(#sprite1-p117)",
         "Lazio": "(#sprite1-p189)",
         "Leeds": "(#sprite1-p27)",
         "Leicester": "(#sprite1-p87)",
         "Leicester City": "(#sprite1-p87)",
         "Liverpool": "(#sprite1-p3)",
         "Lyon": "(#sprite1-p106)",
         "Manchester City": "(#sprite1-p10)",
         "Manchester United": "(#sprite1-p2)",
         "Matchday One": "(#sprite1-p02)",
         "Middlesbrough": "(#sprite1-p91)",
         "MK Dons": "(#sprite1-p332)",
         "Napoli": "(#sprite1-p75)",
         "Newcastle United": "(#sprite1-p11)",
         "Norwich": "(#sprite1-p44)",
         "Norwich City": "(#sprite1-p44)",
         "Nottm Forest": "(#sprite1-p66)",
         "Nottingham Forest": "(#sprite1-p66)",
         "Olympiacos": "(#sprite1-p129)",
         "Ostersunds F": "(#sprite2-p48)",
         "Portsmouth": "(#sprite1-p85)",
         "PSG":"(#sprite1-p35)",
         "Qarabag FK":"(#sprite4-p342)",
         "Real Madrid":"(#sprite1-p9)",
         "Red Star Bel":"(#sprite1-p165)",
         "Rennes":"(#sprite2-p13)",
         "Sevilla": "(#sprite1-p229)",
         "Semi-Final 1L": "(#sprite1-1)",
         "Semi-Final 2L": "(#sprite1-1)",
         "Sheffield United":"(#sprite1-p159)",
         "Southampton": "(#sprite1-p38)",
         "Sporting CP": "(#sprite1-p52)",
         "Standard Liege": "(#sprite1-p351)",
         "Stoke City": "(#sprite1-p81)",
         "Sunderland": "(#sprite1-p46)",
         "Swansea": "(#sprite1-p39)",
         "Tottenham": "(#icon-poop)",
         "Tottenham Hotspur": "(#icon-poop)",
         "Valencia": "(#sprite1-p107)",
         "Vitoria": "(#sprite2-p99)",
         "Watford": "(#sprite1-p112)",
         "West Brom": "(#sprite1-p78)",
         "West Ham United": "(#sprite1-p21)",
         "Wolves": "(#sprite1-p70)",
        }[teamName]

def getComp(comp):
    return {
        "CC":"(#logo-eflcup)",
        "Carabao Cup":"(#logo-eflcup)",
        "Emirates Cup":"(#icon-ball)",
        "Emirates Cup 2019":"(#icon-ball)",
        "English Carabao Cup":"(#logo-eflcup)",
        "Europa League":"(#logo-el)",
        "FA Community Shield":"(#logo-communityshield)",
        "Friendly Match":"(#icon-ball)",
        "International Champions Cup":"(#icon-ball)",
        "Joan Gamper Trophy":"(#icon-ball)",
        "Premier League":"(#logo-pl)",
        "The Emirates FA Cup":"(#logo-facup)",
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


def findFixtures(matches):
    body = ""
    try:
        match = matches[0].find("div",{"class","fixture-match"})
    except IndexError:
        return body
    try:
        date = matches[0].find("time").text
    except:
        date = matches[0].find("div",class_=False, id=False).text.strip()
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
    x = 3
    if len(matches) < 3:
        x = len(matches)
    for i in range(1,x):
        match = matches[i].find("div",{"class","card__content"})
        try:
            date = matches[i].find("div",class_=False, id=False).text.strip()
            time = date.split('-')[1].strip()
            date = date.split('-')[0][3:].strip()
            comp = matches[i].find("div",{"class","event-info__extra"}).text
        except:
            time = "TBD"
            #date = matches[i].find("div",class_=False, id=False).text[3:].strip()
            date = matches[i].find("div",class_=False, id=False).text.strip()
            comp = matches[i].find("div",{"class","event-info__extra"}).text
        try:
            team = match.find("span",{"class","team-crest__name-value"}).text
        except AttributeError:
            team = match.find("div",{"class","team-crest__name-value"}).text
        try:
            location = match.find("div",{"class","location-icon"})['title']
        except TypeError:
            teams = match.findAll("div",{"class","fixture-match__team"})
            homeAway = getLocation(teams)
            if homeAway == 0:
                location = "Home"
            else:
                location = "Away"
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
        try:
            match = matches[i].find("div",{"class","card__content"})
        except:
            if i == 0:
                return body
            break
        try: 
            date = matches[i].find("time").text
        except:
            date = matches[i].find("div",class_=False, id=False).text.strip()
        date = date.split('-')[0][3:].strip()
        comp = matches[i].find("div",{"class","event-info__extra"}).text
        team = match.find("span",{"class","team-crest__name-value"}).text
        location = match.find("div",{"class","location-icon"})['title']
        homeScore = match.findAll("span",{"class","scores__score"})[0].text
        awayScore = match.findAll("span",{"class","scores__score"})[1].text
        if homeScore > awayScore:
            if location == "Home":
                result += "[](#icon-win) "
            elif location == "Neutral":
                if team == "Arsenal":
                    result += "[](#icon-loss) "
                else:
                    result += "[](#icon-win) "
            else:
                result += "[](#icon-loss) "
        elif homeScore < awayScore: 
            if location == "Home":
                result += "[](#icon-loss) "
            elif location == "Neutral":
                if team == "Arsenal":
                    result += "[](#icon-loss)"
                else:
                    result += "[](#icon-win)"
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
    return body

