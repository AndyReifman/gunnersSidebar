#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import praw,re,logging,logging.handlers,datetime,requests,requests.auth,sys,json,unicodedata
from unidecode import unidecode
from praw.models import Message
from collections import Counter
from itertools import groupby
from time import sleep
from bs4 import BeautifulSoup

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


def parseFixture():
    website = "https://www.arsenal.com/fixtures"
    fixtureWebsite = requests.get(website,timeout=15)
    fixture_html = fixtureWebsite.text
    soup = BeautifulSoup(fixture_html, "lxml")
    table = soup.find("div",{"class","accordions"})
    print table.prettify()

parseFixture()
