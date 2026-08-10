#!/usr/bin/python

import datetime
import re

import requests
import requests.auth
from bs4 import BeautifulSoup, ResultSet, Tag


class Match(object):
    date = ""
    homeTeam = ""
    awayTeam = ""
    timeResult = ""
    comp = ""

    def __init__(self, date, homeTeam, awayTeam, timeResult, comp):
        self.date = date
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.timeResult = timeResult
        self.comp = comp


def getLocation(line):
    home_team = line[0].text.strip()
    if "Arsenal" in home_team:
        return 0
    else:
        return 1


def getSprite(team_name):
    return {
        "1. FC Nürnberg": "(#sprite1-p176)",
        "AC Milan": "(#sprite1-p13)",
        "AFC Bournemouth": "(#sprite1-p218)",
        "AFC Wimbledon": "(#sprite1-p145)",
        "Al-Nasr Dubai SC": "(#sprite4-p375",
        "Angers": "(#sprite4-p32)",
        "Arsenal": "(#sprite1-p1)",
        "Aston Villa": "(#sprite1-p19)",
        "Atalanta": "(#sprite2-p182)",
        "Atleti": "(#sprite1-p76)",
        "Atletico Madrid": "(#sprite1-p76)",
        "Atlético de Madrid": "(#sprite1-p76)",
        "Athletic Club": "(#sprite1-p76)",
        "Barcelona": "(#sprite1-p6)",
        "Barnet": "(#sprite1-p245)",
        "Bayern Munich": "(#sprite1-p8)",
        "Bayer 04 Leverkusen": "(#sprite1-p132)",
        "Bayer Leverkusen": "(#sprite1-p132)",
        "Blackpool": "(#sprite1-p146)",
        "Blackpool FC": "(#sprite1-p146)",
        "Bolton Wanderers": "(#sprite1-p104)",
        "Boreham Wood": "(#sprite4-p375)",
        "Bournemouth": "(#sprite1-p218)",
        "BATE": "(#sprite4-p43)",
        "BATE Borisov": "(#sprite4-p43)",
        "Bodø/Glimt": "(#sprite1-p423)",
        "Borussia Dortmund": "(#sprite1-p12)",
        "Brentford": "(#sprite1-p198)",
        "Brentford FC": "(#sprite1-p198)",
        "Brighton": "(#sprite1-p103)",
        "Brighton & Hove Albion": "(#sprite1-p103)",
        "Burnley": "(#sprite1-p156)",
        "Crystal Palace": "(#sprite1-p67)",
        "Cardiff City": "(#sprite1-p80)",
        "Chelsea": "(#sprite1-p4)",
        "Club Brugge": "(#sprite1-p217)",
        "Club Atlético de Madrid": "(#sprite1-p76)",
        "Cologne": "(#sprite1-p125)",
        "Colorado Rapids": "(#sprite1-p93)",
        "Como": "(#sprite5-p341)",
        "Coventry City": "(#sprite1-p136)",
        "CSKA Moscow": "(#sprite1-p220)",
        "Doncaster": "(#sprite1-p252)",
        "Dundalk": "(#sprite2-p143)",
        "Everton": "(#sprite1-p15)",
        "FK Bodø / Glimt": "(#sprite1-p423)",
        "FC Shakhtar Donetsk": "(#sprite1-p294)",
        "FC Vorskla": "(#sprite4-p133)",
        "FC Zürich": "(#sprite3-p5)",
        "Final": "(#sprite1-p02)",
        "Fiorentina": "(#sprite1-p149)",
        "Frankfurt": "(#sprite1-p86)",
        "Girona": "(#sprite4-p254)",
        "GNK Dinamo Zagreb": "(#sprite1-p197)",
        "FK Kairat Almaty": "(#sprite5-p76)",
        "Fulham": "(#sprite1-p29)",
        "Hibernian": "(#sprite1-p164)",
        "Huddersfield Town": "(#sprite1-p199)",
        "Hull City": "(#sprite1-p117)",
        "Internazionale": "(#sprite1-p25)",
        "Inter Milan": "(#sprite1-p25)",
        "Ipswich Town FC": "(#sprite1-p118)",
        "Ipswich Town": "(#sprite1-p118)",
        "Kairat Almaty": "(#sprite5-p76)",
        "Kairat": "(#sprite5-p76)",
        "Lazio": "(#sprite1-p189)",
        "Leeds": "(#sprite1-p27)",
        "Leeds United": "(#sprite1-p27)",
        "Leicester": "(#sprite1-p87)",
        "Leicester City": "(#sprite1-p87)",
        "Liverpool": "(#sprite1-p3)",
        "Luton Town": "(#sprite1-p206)",
        "Lyon": "(#sprite1-p106)",
        "Manchester City": "(#sprite1-p10)",
        "Manchester United": "(#sprite1-p2)",
        "Mansfield Town": "(#sprite2-p248)",
        "Matchday One": "(#sprite1-p02)",
        "Middlesbrough": "(#sprite1-p91)",
        "Millwall": "(#sprite1-p185)",
        "MK Dons": "(#sprite1-p332)",
        "Molde FK": "(#sprite1-p381)",
        "Napoli": "(#sprite1-p75)",
        "Newcastle United": "(#sprite1-p11)",
        "Norwich": "(#sprite1-p44)",
        "Norwich City": "(#sprite1-p44)",
        "Nottm Forest": "(#sprite1-p66)",
        "Nottingham Forest": "(#sprite1-p66)",
        "Olympiacos": "(#sprite1-p139)",
        "Olympique Lyonnais": "(#sprite1-p106)",
        "Orlando City": "(#sprite1-p94)",
        "Ostersunds F": "(#sprite2-p48)",
        "Portsmouth": "(#sprite1-p85)",
        "Port Vale": "(#sprite1-p307)",
        "Preston North End": "(#sprite1-p179)",
        "PSG": "(#sprite1-p35)",
        "Paris Saint-Germain": "(#sprite1-p35)",
        "PSV Eindhoven": "(#sprite1-p120)",
        "Qarabag FK": "(#sprite4-p342)",
        "Rangers": "(#sprite1-p40)",
        "Rapid Vienna": "(#sprite1-p193)",
        "Real Betis": "(#sprite1-p296)",
        "Real Madrid": "(#sprite1-p9)",
        "Real Madrid CF": "(#sprite1-p9)",
        "Red Star Bel": "(#sprite1-p165)",
        "Rennes": "(#sprite2-p13)",
        "Second Round": "(#sprite1-1)",
        "Sevilla": "(#sprite1-p229)",
        "Sevilla FC": "(#sprite1-p229)",
        "Semi-Final 1L": "(#sprite1-1)",
        "Semi-Final 2L": "(#sprite1-1)",
        "Shakhtar Donetsk": "(#sprite1-p294)",
        "Sheffield United": "(#sprite1-p159)",
        "SL Benfica": "(#sprite1-p26)",
        "Slavia Prague": "(#sprite2-p21)",
        "Southampton": "(#sprite1-p38)",
        "Sporting CP": "(#sprite1-p52)",
        "Sporting Clube de Portugal": "(#sprite1-p52)",
        "Standard Liege": "(#sprite1-p351)",
        "Stoke City": "(#sprite1-p81)",
        "Sunderland": "(#sprite1-p46)",
        "Swansea": "(#sprite1-p39)",
        "Tottenham": "(#icon-poop)",
        "Tottenham Hotspur": "(#icon-poop)",
        "Valencia": "(#sprite1-p107)",
        "Villarreal CF": "(#sprite1-p270)",
        "Villarreal": "(#sprite1-p270)",
        "Vitoria": "(#sprite2-p99)",
        "Watford": "(#sprite1-p112)",
        "West Brom": "(#sprite1-p78)",
        "West Bromwich Albion": "(#sprite1-p78)",
        "West Ham United": "(#sprite1-p21)",
        "Wigan Athletic": "(#sprite1-p105)",
        "Wolves": "(#sprite1-p70)",
    }[team_name]


def getComp(comp):
    return {
        "CC": "(#logo-eflcup)",
        "Carabao Cup": "(#logo-eflcup)",
        "Club Friendlies": "(#icon-ball)",
        "Emirates Cup": "(#icon-ball)",
        "Emirates Cup 2019": "(#icon-ball)",
        "English Carabao Cup": "(#logo-eflcup)",
        "Europa League": "(#logo-el)",
        "FA Community Shield": "(#logo-communityshield)",
        "Community Shield": "(#logo-communityshield)",
        "Florida Cup Series": "(#icon-ball)",
        "Florida Cup": "(#icon-ball)",
        "Friendly Match": "(#icon-ball)",
        "International Champions Cup": "(#icon-ball)",
        "Joan Gamper Trophy": "(#icon-ball)",
        "The Mind Series": "(#icon-ball)",
        "Premier League": "(#logo-pl)",
        "The Emirates FA Cup": "(#logo-facup)",
        "English FA Cup": "(#logo-facup)",
        "FA Cup": "(#logo-facup)",
        "UEFA Champions League": "(#logo-ucl)",
    }[comp]


def get_matches() -> ResultSet[Tag]:
    """Retrieve all Arsenal matches this season."""
    website = "https://www.arsenal.com/fixtures/men/printable/20262027"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    }
    fixture_website = requests.get(website, timeout=15, headers=headers)
    fixture_html = fixture_website.text
    soup = BeautifulSoup(fixture_html, "lxml")
    matches = soup.find_all(
        "div", class_=re.compile("printable_printable_hero_box__.*")
    )
    return matches


def parse_opponent(match: Tag) -> tuple:
    """Find the opponent and match location

    Args:
        match: Bs4 Tag containing match participants

    Returns:
        a tuple containing the opponent name and if the match is Home or Away
    """
    details = match.find("div", class_="printable_printable_hero_box_details__JTszY")
    if not details:
        raise ValueError(f"Unable to parse teams for fixture: {match}")
    home = details.find(
        "div", class_=re.compile("printable_printable_hero_box_details_comp1.*")
    )
    away = details.find(
        "div", class_=re.compile("printable_printable_hero_box_details_comp2.*")
    )
    if home:
        home = home.text
    if away:
        away = away.text
    if home == "Arsenal":
        return (away, "Home")
    else:
        return (home, "Away")


def parse_result(match: Tag) -> str:
    """Grabs the scoreline from a match

    Args:
        match: bs4 tag of a match
    Returns:
        A basic scoreline matching x - x format
    """
    result = match.find(
        "div", class_=re.compile("printable_printable_hero_box_details__.*")
    )
    if not result:
        raise ValueError(f"Unable to parse scoreline from match '{match}'")
    scores = result.find(
        "div", class_=re.compile("printable_printable_hero_box_details_result__.*")
    )
    if scores:
        return scores.text


def get_won_or_lost(scoreline, location):
    """Determine if Arsenal won, lost or drew the result"""
    home_score, away_score = map(int, scoreline.split(" - "))
    if location == "Home":
        if home_score > away_score:
            return "W"
        elif home_score < away_score:
            return "L"
    else:
        if home_score > away_score:
            return "L"
        elif home_score < away_score:
            return "W"
    return "D"


def find_fixtures(matches: ResultSet, next_match_index: int):
    """
    Grab the next 3 fixtures for the team
    :param matches: ResultSet
    :return:
    """
    body = ""
    x = 0
    for match in matches[next_match_index:]:
        if x > 2:
            return body
        date = parse_date(match)
        time = date.strftime("%H:%M")
        (opponent, location) = parse_opponent(match)
        team = f"{getSprite(opponent)} ({location[0]})"
        competition_parsed = match.find(
            "div", class_="printable_printable_hero_box_type__JkjSv"
        )
        if competition_parsed:
            comp = competition_parsed.text
        body += (
            "| "
            + date.strftime("%b %d")
            + " | [](#icon-clock) "
            + time
            + " | []"
            + team
            + " | []"
            + getComp(comp)
            + "|\n"
        )
        x += 1
    return body


def find_results(matches: ResultSet, next_match_index: int) -> str:
    """Takes the matches and returns previous results

    Args:
        matches: ResultSet list of all matches in the season
        next_match_index: int index of the next unplayed match in matches

    Returns:
        Markdown formatted string with a table of recent result limited to a maximum of 3 results
    """
    body = ""
    matches = ResultSet(source=None, result=matches[:next_match_index])
    for match in matches[-3:]:
        date = parse_date(match)
        (opponent, location) = parse_opponent(match)
        team = f"{getSprite(opponent)} ({location[0]})"
        competition_parsed = match.find(
            "div", class_=re.compile("printable_printable_hero_box_type__.*")
        )
        if competition_parsed:
            comp = competition_parsed.text
        scoreline = parse_result(match)
        result = get_won_or_lost(scoreline, location)
        result += f" {scoreline}"
        body += (
            "| "
            + date.strftime("%b %d")
            + " | "
            + result
            + " | []"
            + team
            + " | []"
            + getComp(comp)
            + "|\n"
        )

    body += "|||\n"
    return body


def clean_date_string(date_str: str) -> str:
    """Cleans up months abbreviated in ways we don't expect

    Args:
        String representing a date following the Weekday Month Day - HH:MM format

    Returns:
        The same string but with properly abbreviated month.
    """
    # Stupid UK abbreviations
    month_map = {"sept": "Sep"}

    def replace_month(match):
        word = match.group(0)
        return month_map.get(word.lower(), word)

    return re.sub(r"[A-Za-z]+", replace_month, date_str)


def parse_date(match):
    """Return a datetime for the given match

    Args:
        match: A specific match from the Resultset
    Returns:
        Datetimeobject of the match date
    """
    date_string = match.find(
        "div", class_=re.compile("printable_printable_hero_box_date.*")
    ).text
    date_string = clean_date_string(date_string)
    parsed = datetime.datetime.strptime(date_string, "%a %b %d - %H:%M").replace(
        tzinfo=datetime.UTC
    )
    current_year = datetime.datetime.now(tz=datetime.UTC).year
    target_year = current_year if parsed.month >= 7 else current_year + 1
    date = parsed.replace(year=target_year)
    return date


def find_next_match(matches: ResultSet) -> int:
    """Return the index of the next match without a result.

    Args:
        matches: ResultSet containing all matches of the season

    Returns:
        Index in matches of the next fixture to be played
    """
    today = datetime.datetime.now(tz=datetime.UTC)
    for i, match in enumerate(matches):
        date = parse_date(match)
        if date >= today:
            return i
    # If we get here then the season is over and there are no more fixtures
    return -1


def build_body(matches: ResultSet):
    """
    Build the body markdown containing previous results and upcoming fixtures
    """
    # Find index of next match
    next_match_index = find_next_match(matches)
    body = find_results(matches, next_match_index)
    if next_match_index != -1:
        body += find_fixtures(matches, next_match_index)
    return body


def main():
    matches = get_matches()
    body = build_body(matches)
    return body


if __name__ == "__main__":
    print(main())
