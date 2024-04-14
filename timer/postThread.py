#!/usr/bin/python3
# Andrew Reifman-Packett
# June 2020
# Post the Ask Adrian Analysis thread in advance of a match
import calendar
import os

from onebag import login_bot


def createBody(team):
    body = "Good morning everyone, welcome to the Tactics & Analysis Thread for our game against " + team.strip() + ".\n\n"
    body += "This thread is designed for reasoned, level-headed and non-abusive analysis and reaction during the build-up, the game itself, and the post-match reaction. We will be keeping a close eye on this thread to ensure this thread stays a place for that - if you want your normal match-day experience, the pre-, post-, and match threads will be running today as normal.\n\n"
    body += "Don't forget, this is also an opportunity for the sub to be involved in the Arsenal.com matchday experience; possibly providing content for Adrian Clarke's new show, The Breakdown LIVE. There's a chance that content from this thread will be used in the show, so play nice. You can either submit a question for Adrian or ask his opinion on a piece of analysis you have done yourself.\n\n"
    body += "You can also use the form on the [AskAdrian page on arsenal.com](https://www.arsenal.com/askadrian) to submit a question - make sure to let them know we sent you!"
    return body

def findTeam(summary):
    teams = summary.split(' v ')
    for team in teams:
        team = team.split('(')[0]
        if 'Arsenal' not in team:
            return team


def main(summary, date):
    r,subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    date = date.split('-')
    date = date[2] + " " + calendar.month_abbr[int(date[1])] + " " + date[0]
    title = "Tactics & Analysis Thread: " + summary + " [" + date + "]"
    team = findTeam(summary)
    body = createBody(team)
    r.subreddit(subreddit).submit(title,selftext=body,send_replies=False)


if __name__ == '__main__':
    main()
