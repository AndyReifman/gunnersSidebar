#!/usr/bin/python3

# ANDREW REIFMAN-PACKETT
# December 2020
# The new reddit AutoScheduler lacks several very basic functionality that
#   we take advantage of in /r/gunners. Creating this script to accomplish
#   what we need on our own without relying on them.

import datetime,praw,time

def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t

def loginBot():
    try:
        f = open('/home/andy/reddit/sidebar/login.txt')
        subreddit,user_agent,id,secret,refresh = f.readline().split('||',8)
        f.close()
        r = praw.Reddit(client_id = id,
                client_secret = secret,
                refresh_token = refresh.strip(),
                user_agent = user_agent)
        print(getTimestamp() + "Oauth session opened as /u/" + r.user.me().name)
    except Exception as e:
        print(getTimestamp() + str(e))
        print(getTimestamp() + "Setup error in discussion threads.\n")
        exit()

    return r,'eabryt'

def createBody():
    body = "Use this thread for general daily football discussion.\n\n"
    body += "This thread can also be used to discuss Transfer rumours and to post Tier 4 sources.\n\n"
    body += "As this may fill up please sort by new to try and avoid constantly repeating the same question.\n\n"
    body += "Join our [Discord](https://discord.gg/gunners) for live discussion and don't forget to follow us on [twitter](https://twitter.com/rslashgunners).\n\n"
    return body

def pinnedComment():
    body = "Reminder: These threads are to help promote discussion and varying points of view. Low-effort comments or jokes can & will be removed with no reason necessary.\n\n"
    body += "*I am a \"bot\", and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/Gunners) if you have any questions or concerns.*"
    return body

def createTitle():
    date = datetime.date.today().strftime('%B %d, %Y')
    title = date + " Daily Discussion & Transfers Thread"
    return title

def main():
    title = createTitle()
    body = createBody()
    comment = pinnedComment()
    r,subreddit = loginBot()
    post = r.subreddit(subreddit).submit(title,selftext=body,send_replies=False)
    post.comment_sort = "new"
    comment = post.reply(comment)
    comment.mod.distinguish(sticky=True)

if __name__ == '__main__':
    main()
