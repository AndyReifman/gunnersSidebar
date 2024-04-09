# Scripts for updating the [/r/gunners](https://old.reddit.com/r/gunners) subreddit sidebar.

These scripts update the Fixtures & Results, Premier League, Goals, Assists, and Injuries tables in the subreddit sidebar.

# Installation

You will need an understanding of reddit PRAW and be set up to log in. I use a file called login.txt which looks like

```bash
<subreddit>:<user_agent>:<id>:<secret>:<refresh_token>
```

# Usage
Most of the scripts scrape data from arsenal.com unless noted.

## Fixtures & Results table
Scrape the fixtures & results pages for the last 3 matches and the 3 matches upcoming.
Get the result or KO time and format it to display nicely in a table.
It can be updated to use any other website, however you will need to most likely make several changes to the web scraping.

## Premier League Table
Scrapes arsenal.com's Premier League table, generally shows 5 teams (including Arsenal) which requires some easy math to get the correct number of teams above/below depending on Arsenal's position in the table.
There is also a script set up for getting the Europa League table from ESPNFC, however it has not been updated since 2018 so I am unsure if it still works.

## Goals & Assists tables
The Goals table is created by scraping through the statistics page on arsenal.com. While the sidebar only shows the top 5 scorers I simply create an array that contains all the goals for all the players and sort by total goals, then print out the first 5.

The Assists table is a bit more complicated. Arsenal.com doesn't maintain those stats so I get them from TransferMarkt.com. I have to do way more scraping via BeautifulSoup and will need to update the URLs every season if I don't decide to create the URL programmatically.

## Injuries Table
I used to have access to an API for this however the owners of the API stopped updating their website so we find ourselves going back to TransferMarkt for the injury information.
TransferMarkt's website is a mess but BeautifulSoup makes things easier. Just grab the whole injury table and loop through it to build our own table that we want to use for the sidebar
