#!/usr/bin/python
# -*- coding: utf-8 -*-


import praw,urllib,re,logging,logging.handlers,datetime,requests,requests.auth,sys,json,unicodedata
from praw.models import Message
from collections import Counter
from itertools import groupby
from time import sleep
from bs4 import BeautifulSoup

def getSprite(teamName):
    return {
         "Arsenal": "(#sprite1-p1)",
         "BATE Borisov":"(#sprite4-p43)",
         "FC Cologne":"(#sprite1-p125)",
         "FK Qarabag":"(#sprite4-p342)",
         "Red Star Belgrade":"(#sprite1-p165)",
         "Sporting CP":"(#sprite1-p52)",
         "Vorskla":"(#sprite4-p342)",
        }[teamName]


def getSign(goalDiff):
    if int(goalDiff) > 0:
        return "+"+goalDiff
    return goalDiff




def buildTable(table):
    body = ""
    for row in table.findAll("tr",attrs={'style':'background-color: #FFFFFF'}):
        cells = row.findAll("td")
        position = cells[0].find(text=True)
        try:
            team = cells[1].find("a").find(text=True)
        except:
            team = cells[1].find(text=True).strip()
        goalDiff = cells[22].find(text=True)
        points = cells[23].find(text=True)
        body += "|**"+position+"**|[]"+getSprite(team)+"|"+getSign(goalDiff)+"|"+points+"|\n"
    return body

def parseWebsite():
    website = "http://www.espnfc.us/uefa-europa-league/2310/group/5/group-e"
    tableWebsite = requests.get(website, timeout=15)
    table_html = tableWebsite.text
    soup = BeautifulSoup(table_html, "lxml")
    table = soup.find("div",{"class","responsive-table-content"})
    table = table.find("tbody")
    return table

def main():
    table = parseWebsite()
    body = buildTable(table)
    return body
