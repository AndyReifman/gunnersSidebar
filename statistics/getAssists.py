#!/usr/bin/python
# -*- coding: utf-8 -*-

from unidecode import unidecode
import requests,re,datetime

players = [0] * 5
totalAssists = [0] * 5

def getTimestamp():
        dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
        hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
        min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
        t = '[' + hr + ':' + min + '] '
        return dt + t

def getStats(player,html,i):
    body = "|"
    assists = totalAssists[i]
    line = html.split('<div class="stats-top-scores">')[1]
    #playerLine = re.findall('<td headers="player"><a href=.*>(.*)<\/a><\/td>',line)[0]
    playerLine = line.split('<tr>')[2:]
    for x in range(0,len(playerLine)):
        name = re.findall('<td headers="player"><a href=.*>(.*)<\/a><\/td>',playerLine[x])[0]
        if name == player:
            body += re.findall('<td headers="goals">([0-9])</td>',playerLine[x])[0]
            totalAssists[i] += int(re.findall('<td headers="goals">([0-9])</td>',playerLine[x])[0])
    if assists == totalAssists[i]:
        body += "0"
    return body


def parseWebsite():
    website = "http://www.espnfc.us/club/arsenal/359/statistics/assists?leagueId=all"
    goalsWebsite = requests.get(website, timeout=15)
    goals_html = goalsWebsite.text
    scorersList = goals_html.split('<div class="stats-top-scores">')[1]
    topScorers = scorersList.split('<tr>')[2:]
    for i in range(0,5):
        players[i] = re.findall('<td headers="player"><a href=.*>(.*)<\/a><\/td>',topScorers[i])[0]
    return players

def parseStats(player, i):
    body = ""
    premierLeague = "http://www.espnfc.us/club/arsenal/359/statistics/assists?leagueId=23"
    faCup = "http://www.espnfc.us/club/arsenal/359/statistics/assists?leagueId=40"
    europaLeague = "http://www.espnfc.us/club/arsenal/359/statistics/assists?leagueId=2310"
    eflCup = "http://www.espnfc.us/club/arsenal/359/statistics/assists?leagueId=41"
    premierLeagueWebsite = requests.get(premierLeague, timeout=15)
    faCupWebsite = requests.get(faCup, timeout=15)
    europaLeagueWebsite = requests.get(europaLeague, timeout=15)
    eflCupWebsite = requests.get(eflCup, timeout=15)
    premier_html = premierLeagueWebsite.text
    fa_html = faCupWebsite.text
    europa_html = europaLeagueWebsite.text
    efl_html = eflCupWebsite.text
    #Premier League
    year = re.findall('<p class="dropdown-value"><span>(.*)</span></p>',premier_html)[1]
    if year == "2017/2018":
        try: 
            body += getStats(player,premier_html,i)
        except:
            print getTimestamp() + "No Premier League assists found"
            body += "|0"
    else:
        body += "|0"
    #Europa League
    year = re.findall('<p class="dropdown-value"><span>(.*)</span></p>',europa_html)[1]
    if year == "2017/2018":
        try: 
            body += getStats(player,europa_html,i)
        except:
            print getTimestamp() + "No Europa League assists found"
            body += "|0"
    else:
        body += "|0"
    #FA Cup
    year = re.findall('<p class="dropdown-value"><span>(.*)</span></p>',fa_html)[1]
    if year == "2017/2018":
        try:
            body += getStats(player,fa_html, i)
        except:
            print getTimestamp() + "No FA Cup assists found"
            body += "|0"
    else:
        body += "|0"
    #EFL Cup
    year = re.findall('<p class="dropdown-value"><span>(.*)</span></p>',efl_html)[1]
    if year == "2017/2018":
        try:
            body += getStats(player,efl_html,i)
        except:
            print getTimestamp() + "No EFL Cup assists found"
            body += "|0"
    else:
        body += "|0"
    body += "|"+str(totalAssists[i])+"|\n"
    if totalAssists[i] == 0:
        return ""
    return body

def buildTable(players):
    body = ""
    for i,player in enumerate(players):
        temp = player.replace(' ','-').lower()
        temp = unidecode(temp)
        newLine = parseStats(player,i)
        if newLine == "":
            continue
        else:  
            if unidecode(temp) == 'alexis-sanchez':
                temp = "alexis"
            body += "|["+player+"](http://www.arsenal.com/arsenal/players/"+temp+")"
            body += newLine
    return body


def main():
    players = parseWebsite()
    body = buildTable(players)
    return body
