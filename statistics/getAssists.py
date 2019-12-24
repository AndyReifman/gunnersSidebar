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
    table = soup.find("table",{"class":"items"})
    stats = table.find("tbody")
    for row in stats.findAll("tr",{"class":['odd','even']}):
        player = ""
        #First up, get the name
        name = row.find("td",{"class":"posrela"}).findAll("a",{"class":"spielprofil_tooltip"})[0].getText()
        columns = row.findAll("td",{"class":"zentriert"})
        try:
            assists = columns[6].getText()
        except:
            assists = 0
        if (assists == "-"):
            assists = 0
        #assists = totalAssists[i]
        #League 
        found = 0
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
                    updateTable(p)
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
                    updateTable(p)
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,0,assists,0,int(assists))
                updateTable(player)
        #EFL Cup
        if comp == 3:
            #Check to see if player already exists in the table
            for index,p in enumerate(players):
                if p.name == name:
                    p.eflcup = assists
                    p.total += int(assists)
                    found = 1
                    updateTable(p)
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,0,0,assists,int(assists))
                updateTable(player)
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
    total = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=%262019"
    premierLeague = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=GB1%262019"
    #faCup = ""
    europaLeague = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=EL%262019"
    eflCup = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=CGB%262019"
    premierLeagueWebsite = requests.get(premierLeague,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    #faCupWebsite = requests.get(faCup,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    europaLeagueWebsite = requests.get(europaLeague,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    eflCupWebsite = requests.get(eflCup,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    premier_html = premierLeagueWebsite.text
    #fa_html = faCupWebsite.text
    europa_html = europaLeagueWebsite.text
    efl_html = eflCupWebsite.text
    #Premier League
    getStats(premier_html,0)
    #Europa League
    getStats(europa_html,1)
    #FA Cup
    #FA Cup starts in 2020
    getStats(efl_html,3)
    #body += "|"+str(totalAssists[i])+"|\n"
    #players.sort(key=lambda x: x.total, reverse=True)

def buildTable():
    body = ""
    for x in range(0, 5):
        p = players[x]
        player = p.name
        temp = player.replace(' ','-').lower()
        try:
            temp = unidecode(temp)
        except:
            pass
        newLine = str(p.league)+"|"+str(p.europa)+"|"+str(p.facup)+"|"+str(p.eflcup)+"|"+str(p.total)+"|\n"
        if newLine == "":
            continue
        else:  
            try:
                if unidecode(temp) == 'alexis-sanchez':
                    temp = "alexis"
            except:
                pass
            body += "|["+player+"](http://www.arsenal.com/arsenal/players/"+temp+")|"
            body += newLine
    return body


def main():
    parseStats()
    body = buildTable()
    return body
