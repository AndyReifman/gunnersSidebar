#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

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

def printPlayers():
    for x in range(len(players)):
        p = players[x]
        print(p.name +": " + str(p.league) +" " + str(p.champions) + " " + str(p.facup) + " " + str(p.eflcup) + " " + str(p.total))

def printPlayer(p):
    print(p.name +": " + str(p.league) +" " + str(p.champions) + " " + str(p.facup) + " " + str(p.eflcup) + " " + str(p.total))
 

def getStats(html,comp):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table",{"class":"items"})
    stats = table.find("tbody")
    for row in stats.findAll("tr",{"class":['odd','even']}):
        player = ""
        #First up, get the name
        #name = row.find("td",{"class":"posrela"}).findAll("a",{"class":"spielprofil_tooltip"})[0].getText()
        name = row.find("td",{"class":"hauptlink"}).find_all('a', href=True)[0].getText()
        columns = row.findAll("td",{"class":"zentriert"})
        try:
            goals = columns[5].getText()
        except:
            goals = 0
        if (goals == "-"):
            goals = 0
        #goals = totalAssists[i]
        #League 
        found = 0
        if comp == 0:
            player = Player(name,goals,0,0,0,int(goals))
            players.append(player)
        #Champions League
        if comp == 1:
            #Check to see if player already exists in the table
            for index,p in enumerate(players):
                if p.name == name:
                    p.champions = goals
                    p.total += int(goals)
                    found = 1
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,goals,0,0,int(goals))
                players.append(player)
        #FA Cup
        if comp == 2:
            #Check to see if player already exists in the table
            for index,p in enumerate(players):
                if p.name == name:
                    p.facup = goals
                    p.total += int(goals)
                    found = 1
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,0,goals,0,int(goals))
                players.append(player)
        #EFL Cup
        if comp == 3:
            #Check to see if player already exists in the table
            for index,p in enumerate(players):
                if p.name == name:
                    p.eflcup = goals
                    p.total += int(goals)
                    found = 1
                    break
            #If the player doesn't exist we need to create them.
            if not found:
                player = Player(name,0,0,0,goals,int(goals))
                players.append(player)
    return 

def parseStats():
    body = ""
    total = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=%262024"
    premierLeague = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=GB1%262024"
    faCup = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=FAC%262024"
    champions_league = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=CL%262024"
    eflCup = "https://www.transfermarkt.us/arsenal-fc/leistungsdaten/verein/11/plus/1?reldata=CGB%262024"
    premierLeagueWebsite = requests.get(premierLeague,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    faCupWebsite = requests.get(faCup,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    champions_league_website = requests.get(champions_league,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    eflCupWebsite = requests.get(eflCup,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    premier_html = premierLeagueWebsite.text
    fa_html = faCupWebsite.text
    champions_html = champions_league_website.text
    efl_html = eflCupWebsite.text
    #Premier League
    getStats(premier_html,0)
    #Europa League
    getStats(champions_html,1)
    #FA Cup
    getStats(fa_html,2)
    #EFL Cup
    getStats(efl_html,3)

def buildTable():
    players.sort(key=lambda x: x.total, reverse=True)
    body = ""
    for x in range(0, 5):
        p = players[x]
        player = p.name
        temp = player.replace(' ','-').lower()
        try:
            temp = unidecode(temp)
        except:
            pass
        newLine = str(p.league) +"|" + str(p.champions) + "|" + str(p.facup) + "|" + str(p.eflcup) + "|" + str(p.total) + "|\n"
        if newLine == "":
            continue
        else:  
            try:
                if unidecode(temp) == 'alexis-sanchez':
                    temp = "alexis"
            except:
                pass
            body += "|["+player+"](http://www.arsenal.com/men/players/"+temp+")|"
            body += newLine
    return body


def main():
    parseStats()
    body = buildTable()
    return body

if __name__ == "__main__":
    main()

