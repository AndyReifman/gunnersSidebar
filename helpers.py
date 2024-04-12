import datetime
import os
from time import sleep

import praw


def getTimestamp():
    """
    Returns the current timestamp for logging
    :return: timestamp: Format of m/dd [hh:mm]
    """
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(
        datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(
        datetime.datetime.now().minute)
    t = '[' + hr + ':' + minute + '] '
    return dt + t


def loginBot():
    """
    Create a reddit instance from login.txt
    :return: (reddit instance, subreddit to use)
    """
    try:
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login.txt'), 'r')
        subreddit, user_agent, client_id, secret, refresh = f.readline().split('||', 5)
        f.close()
        r = praw.Reddit(client_id=client_id,
                        client_secret=secret,
                        refresh_token=refresh.strip(),
                        user_agent=user_agent)

        print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
    except Exception as e:
        print(getTimestamp() + str(e))
        print(getTimestamp() + "Setup error in Results \n")
        sleep(1)
        exit()

    return r, subreddit
