#!/usr/bin/python3
# -*- coding: utf-8 -*-

import praw, re, datetime, requests
from bs4 import BeautifulSoup


def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(
        datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(
        datetime.datetime.now().minute)
    t = '[' + hr + ':' + minute + '] '
    return dt + t


def loginBot():
    f = open('../login.txt')
    subreddit, user_agent, client_id, secret, refresh = f.readline().split('||', 5)
    f.close()
    r = praw.Reddit(client_id=client_id,
                    client_secret=secret,
                    refresh_token=refresh.strip(),
                    user_agent=user_agent)
    print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
    return r, 'gunners'


def getNum(name):
    return {
        "Bernd Leno": "1",
        "Hector Bellerin": "2",
        "Kieran Tierney": "3",
        "Sokratis": "5",
        "Henrikh Mkhitaryan": "7",
        "Dani Ceballos": "8",
        "Gabriel Jesus": "9",
        "Mesut Ozil": "10",
        "Lucas Torreira": "11",
        "Jurrien Timber": "12",
        "Pierre-Emerick Aubameyang": "14",
        "Ainsley Maitland-Niles": "15",
        "Rob Holding": "16",
        "Nicolas Pepe": "19",
        "Shkodran Mustafi": "20",
        "Calum Chambers": "21",
        "David Luiz": "23",
        "Reiss Nelson": "24",
        "Mohamed Elneny": "25",
        "Emiliano Martinez": "26",
        "Konstantinos Mavropanos": "27",
        "Joe Willock": "28",
        "Matteo Guendouzi": "29",
        "Sead Kolasinac": "31",
        "Matt Macey": "33",
        "Granit Xhaka": "34",
        "Gabriel Martinelli": "35",
        "Bukayo Saka": "77",
    }[name]


def getInjuries():
    body = ''
    address = 'https://www.transfermarkt.com/arsenal-fc/sperrenundverletzungen/verein/11'
    website = requests.get(address, headers={'User-Agent': 'Custom'})
    html = website.text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"class", "items"}).find("tbody")
    rows = table.findAll("tr", {"class", "odd","even"})

    for row in rows:
        if 'extrarow bg_blau_20 hauptlink' in str(row):
            return body
        name = row.find('td', {'class', 'hauptlink'}).text.strip()
        injury = row.find('td', {'class', 'links hauptlink img-vat'}).getText()

        date = row.findAll('td', {'class', 'zentriert'})[2].getText()
        if date == '?':
            date = 'Unknown'
        num = getNum(name)
        body += '|' + num + '|' + name + '|' + injury + '|' + date + '|\n'
    return body


def buildTable():
    body = "[//]: # (Injury Table)\n"
    body += "|\\#| Player | Injury | Estimated Return |\n"
    body += "|:------:|:------:|:-------:|:---------:|\n"
    body += getInjuries()
    body += "[//]: # (End Injury Table)"
    return body


def updateSidebar():
    table = buildTable()
    print(getTimestamp() + table)
    r, subreddit = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Injury Table\).*\[\/\/\]: # \(End Injury Table\)', table, contents,
                      flags=re.DOTALL)
    r.subreddit(subreddit).mod.update(description=contents)
    print(getTimestamp() + "Injury Table Updated")


def main():
    updateSidebar()


if __name__ == '__main__':
    main()
