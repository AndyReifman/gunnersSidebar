#!/usr/bin/python3
import os.path

import bs4.element
import praw
import requests
import re
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
from onebag import get_timestamp, login_bot

currency_type = {
    '€': 'EUR',
    '$': 'USD',
    '£': 'GBP'
}

convert_club = {
    "Brentford FC": "Brentford",
    "Fluminense": "Fluminense",
    "Nottm Forest": "Nottingham Forest",
    "Real Sociedad": "Real Sociedad",
}
def get_transfers_table():
    address = 'https://www.transfermarkt.com/arsenal-fc/transfers/verein/11/saison_id/2024'
    website = requests.get(address, headers={'User-Agent': 'Custom'})
    html = website.text
    soup = BeautifulSoup(html, 'lxml')
    boxes = soup.find_all('div','box')
    transfers = [div for div in boxes if div.find('h2') and re.compile(r'Arrivals|Departures').search(div.find('h2').text)]
    return transfers

def convert_price(cost):
    if 'free transfer' in cost:
        return 'Free'
    if 'loan' in cost:
        return 'Loan'
    if '-' in cost:
        return 'End of Contract'
    pattern = re.compile(r'([€$£])([\d,.]+)([mk]?)')
    match = pattern.match(cost)
    if not match:
        raise ValueError(f"Transfer price: {cost} is invalid format.")
    currency, amount, magnitude = match.groups()
    amount = float(amount.replace(',',''))
    if magnitude == 'm':
        amount *= 1_000_000
    elif magnitude == 'k':
        amount *= 1_000
    cost = CurrencyConverter().convert(amount, currency_type[currency], 'GBP')
    if cost >= 1_000_000:
        return f"£{cost / 1_000_000:.2f}m"
    elif cost >= 1_000:
        return f"£{cost / 1_000:.2f}k"
    else:
        return f"£{cost:.2f}"


def parse_player_name(cell):
    table = cell.find('table')
    return table.find('a', href=re.compile(r'profil')).text

def parse_player_club(cell):
    table = cell.find('table')
    club = table.find('a', href=re.compile(r'startseite'))['title']
    if 'Without Club' in club:
        club = 'N/A'
    return club

def parse_table(arrivals):
    body = ''
    table = arrivals.find('table', class_='items').find('tbody')
    for row in table.find_all('tr', recursive=False):
        cols = row.find_all('td', recursive=False)
        cost = cols[5].text
        if 'End of loan' in cost:
            continue
        cost = convert_price(cols[5].text)
        player = parse_player_name(cols[1])
        club = parse_player_club(cols[4])
        body += f'| {player} | {club} | {cost} |\n'
    return body

def build_arrivals_table(arrivals: bs4.element.Tag):
    body = "[//]: # (Men's Arrivals)\n"
    body += "| Name | Club | Transfer Sum |\n"
    body += "|:------:|:-------:|:---------:|\n"
    body += parse_table(arrivals)
    body += "[//]: # (End Men's Arrivals)"
    return body

def build_departures_table(departures: bs4.element.Tag):
    body = "[//]: # (Men's Departures)\n"
    body += "| Name | Club | Transfer Sum |\n"
    body += "|:------:|:-------:|:---------:|\n"
    body += parse_table(departures)
    body += "[//]: # (End Men's Departures)"
    return body

def build_tables():
    transfers = get_transfers_table()
    arrivals = build_arrivals_table(transfers[0])
    print(get_timestamp() + arrivals)
    departures = build_departures_table(transfers[1])
    print(get_timestamp() + departures)
    return arrivals, departures
def updateSidebar():
    arrivals, departures = build_tables()
    r, subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/]: # \(Mens Arrivals\).*\[\/\/]: # \(End Mens Arrivals\)', arrivals, contents,
                      flags=re.DOTALL)
    contents = re.sub('\[\/\/\]: # \(Mens Departures\).*\[\/\/\]: # \(End Mens Departures\)', departures, contents,
                      flags=re.DOTALL)
    r.subreddit(subreddit).mod.update(description=contents)
    print(get_timestamp() + "Men's Transfer Tables Updated")

def main():
    updateSidebar()


if __name__ == '__main__':
    main()
