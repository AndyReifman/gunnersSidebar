#!/usr/bin/python
# -*- coding: utf-8 -*-

from unidecode import unidecode
import requests,re
import datetime
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

def parseWebsite():
    website = "https://www.arsenal.com/first-team/statistics"
    goalsWebsite = requests.get(website,timeout=15)
    html = goalsWebsite.text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("div",{"class": "card__content"})
    for row in table.findAll("tr")[2:]:
        cells = row.findAll("td")
        name = cells[0].find(text=True)
        league = cells[2].find(text=True)
        europa = cells[6].find(text=True)
        facup = cells[8].find(text=True)
        eflcup = cells[10].find(text=True)
        total = cells[14].find(text=True)
        player = Player(name,league,europa,facup,eflcup,total)
        if player.total != 0:
            updateTable(player)

def updateTable(player):
    for index,p in enumerate(players):
        if int(player.total) >= int(p.total):
            players.insert(index,player)
            return
    players.append(player)
    return

def printPlayers():
    for x in range(0, 5):
        p = players[x]
        print p.name+": "+p.league+" "+p.europa+" "+p.facup+" "+p.eflcup+" "+p.total

def buildTable():
    body = ""
    for x in range(0, 5):
        p = players[x]
        temp = p.name.replace(' ','-').lower()
        body +="|["+p.name+"](http://www.arsenal.com/arsenal/players/"+temp+")"
        body +="|"+p.league+"|"+p.europa+"|"+p.facup+"|"+p.eflcup+"|"+p.total+"|\n"
    return body
    


def main():
    parseWebsite()
    body = buildTable()
    return body
