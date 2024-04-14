#!/usr/bin/python3
import os.path
# ANDREW REIFMAN-PACKETT
# December 2020
# The new reddit AutoScheduler lacks several very basic functionality that
#   we take advantage of in /r/gunners. Creating this script to accomplish
#   what we need on our own without relying on them.

from datetime import datetime

from onebag import login_bot


def createBody():
    body = "Use this thread for general daily football discussion.\n\n"
    body += "This thread can also be used to discuss Transfer rumours and to post Tier 4 sources.\n\n"
    body += "As this may fill up please sort by new to try and avoid constantly repeating the same question.\n\n"
    body += "Join our [Discord](https://discord.gg/gunners) for live discussion and don't forget to follow us on [twitter](https://twitter.com/rslashgunners).\n\n"
    return body


def pinnedComment():
    body = "Reminder: These threads are to help promote discussion and varying points of view. Low-effort comments or jokes can & will be removed with no reason necessary.\n\n"
    body += "*I am a \"bot\", and this action was performed automatically. This account is not monitored. Please [contact the moderators of this subreddit](/message/compose/?to=/r/Gunners) if you have any questions or concerns.*"
    return body


def createTitle():
    date = datetime.today().strftime('%B %d, %Y')
    title = date + " Daily Discussion & Transfers Thread"
    return title, (datetime.now().isoweekday() in range(1, 6))


def main():
    title, weekday = createTitle()
    body = createBody()
    comment = pinnedComment()
    r, subreddit = login_bot(os.path.dirname(os.path.dirname(__file__)))
    post = r.subreddit(subreddit).submit(title, selftext=body, send_replies=False)
    post.mod.suggested_sort(sort="new")
    # if weekday:
    post.mod.sticky()
    comment = post.reply(comment)
    comment.mod.distinguish(sticky=True)


if __name__ == '__main__':
    main()
