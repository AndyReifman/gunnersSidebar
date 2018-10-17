#!/usr/bin/python
# -*- coding: utf-8 -*-

from unidecode import unidecode
import requests,re,datetime
from bs4 import BeautifulSoup

players = []

class Player(object):
    name = ""
    league = 0
    europa = 0
    facup = 0
    eflcup = 0
    total = 0

    def __init__(self,name,league,europa,facup,eflcup,total):
        self.name = name
        self.league = league
        self.europa = europa
        self.facup = facup
        self.eflcup = eflcup
        self.total = total


def getTimestamp():
        dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
        hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
        t = '[' + hr + ':' + min + '] '
        return dt + t

def printPlayers():
    for x in range(len(players)):
        p = players[x]
        print p.name+": "+str(p.league)+" "+str(p.europa)+" "+str(p.facup)+" "+str(p.eflcup)+" "+str(p.total)

def printPlayer(p):
    print p.name+": "+str(p.league)+" "+str(p.europa)+" "+str(p.facup)+" "+str(p.eflcup)+" "+str(p.total)
 

def getStats(html,comp):
    soup = BeautifulSoup(html, "lxml")
    table = soup.findAll("tbody",{"class":"Table2__tbody"})[1]
    #assists = totalAssists[i]
    player = ""
    for row in table.findAll("tr"):
        found = 0
        cells = row.findAll("td")
        name = cells[1].find(text=True)
        assists = cells[3].find(text=True)
        #League 
        if comp == 0:
            player = Player(name,assists,0,0,0,int(assists))
            updateTable(player)
        #Europa
        if comp == 1:
            #Check to see if player already exists in the table
            for p in players:
                if p.name == name:
                    p.europa = assists
                    p.total += int(assists)
                    found = 1
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,assists,0,0,int(assists))
                updateTable(player)
        #FA Cup
        if comp == 2:
            #Check to see if player already exists in the table
            for index,p in enumerate(players):
                if p.name == name:
                    p.facup = assists
                    p.total += int(assists)
                    found = 1
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,0,assists,0,int(assists))
        #EFL Cup
        if comp == 3:
            #Check to see if player already exists in the table
            for index,p in enumerate(players):
                if p.name == name:
                    p.eflcup = assists
                    p.total += int(assists)
                    found = 1
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,0,0,assists,int(assists))
    return 

def updateTable(player):
    for index,p in enumerate(players):
        if int(player.total) >= (p.total):
            players.insert(index,player)
            return
    players.append(player)
    return

def parseStats():
    body = ""
    premierLeague = "http://www.espn.com/soccer/team/stats/_/id/359/league/ENG.1"
    faCup = "http://www.espn.com/soccer/team/stats/_/id/359/league/ENG.FA"
    europaLeague = "http://www.espn.com/soccer/team/stats/_/id/359/league/UEFA.EUROPA"
    eflCup = "http://www.espn.com/soccer/team/stats/_/id/359/league/ENG.LEAGUE_CUP"
    premierLeagueWebsite = requests.get(premierLeague, timeout=15)
    faCupWebsite = requests.get(faCup, timeout=15)
    europaLeagueWebsite = requests.get(europaLeague, timeout=15)
    eflCupWebsite = requests.get(eflCup, timeout=15)
    premier_html = premierLeagueWebsite.text
    fa_html = faCupWebsite.text
    europa_html = europaLeagueWebsite.text
    efl_html = eflCupWebsite.text
    #Premier League
    getStats(premier_html,0)
    #Europa League
    getStats(europa_html,1)
    #FA Cup
    #FA Cup starts in 2019
    #EFL Cup
    getStats(efl_html,3)
    #body += "|"+str(totalAssists[i])+"|\n"
    players.sort(key=lambda x: x.total, reverse=True)

def buildTable():
    body = ""
    for x in range(0, 5):
        p = players[x]
        player = p.name
        temp = player.replace(' ','-').lower()
        temp = unidecode(temp)
        newLine = str(p.league)+"|"+str(p.europa)+"|"+str(p.facup)+"|"+str(p.eflcup)+"|"+str(p.total)+"|\n"
        if newLine == "":
            continue
        else:  
            if unidecode(temp) == 'alexis-sanchez':
                temp = "alexis"
            body += "|["+player+"](http://www.arsenal.com/arsenal/players/"+temp+")|"
            body += newLine
    return body


def main():
    parseStats()
    body = buildTable()
    return body
