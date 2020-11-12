<<<<<<< HEAD
#!/usr/bin/python3
=======
#!/usr/bin/python2.7
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
'''
' Andrew Reifman-Packett
' May 2017
'''
import getGoals
import getAssists
import praw
import datetime
import time
import re
<<<<<<< HEAD
=======
import pyotp
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
from time import sleep

def getTimestamp():
    dt = str(datetime.datetime.now().month) + '/' + str(datetime.datetime.now().day) + ' '
    hr = str(datetime.datetime.now().hour) if len(str(datetime.datetime.now().hour)) > 1 else '0' + str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) > 1 else '0' + str(datetime.datetime.now().minute)
    t = '[' + hr + ':' + min + '] '
    return dt + t

def loginBot():
    try:
<<<<<<< HEAD
        f = open('/home/andy/reddit/sidebar/login.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect,refresh = f.readline().split('||',8)
        f.close()
=======
        f = open('/root/reddit/sidebar/login.txt')
        fkey = open('/root/reddit/sidebar/2fakey.txt')
        admin,username,password,subreddit,user_agent,id,secret,redirect,refresh = f.readline().split('||',8)
        key = fkey.readline().rstrip()
        totp = pyotp.TOTP(key)
        password += ':'+totp.now()
        f.close()
        fkey.close()
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
        r = praw.Reddit(client_id=id,
             client_secret=secret,
             refresh_token=refresh.strip(),
             user_agent=user_agent)
<<<<<<< HEAD
        print(getTimestamp() + "OAuth session opened as /u/" + r.user.me().name)
        return r,admin,username,password,subreddit,user_agent,id,secret,redirect
    except Exception as e:
        print(getTimestamp() + str(e))
        print(getTimestamp() + "Setup error in statistics\n")
=======
        print getTimestamp() + "OAuth session opened as /u/" + r.user.me().name
        return r,admin,username,password,subreddit,user_agent,id,secret,redirect
    except Exception, e:
        print getTimestamp() + str(e)
        print getTimestamp() + "Setup error in statistics\n"
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321
        sleep(5)
        exit()

def buildGoalSidebar():
    body = "[//]: # (Goals Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += getGoals.main()
    body += "[//]: # (End Goals Table)"
    return body

def buildAssistsSidebar():
    body = "[//]: # (Assists Table)\n"
    body += "| Player | [](#logo-pl) | [](#logo-el) | [](#logo-facup) | [](#logo-eflcup)| Total |\n"
    body += "|:----:|:----:|:----:|:----:|:----:|:----:|\n"
    body += getAssists.main()
    body += "[//]: # (End Assists Table)"
    return body


def updateGoals():
    goals = buildGoalSidebar()
    assists = buildAssistsSidebar()
    r,admin,username,password,subreddit,user_agent,id,secret,redirect = loginBot()
    settings = r.subreddit(subreddit).mod.settings()
    contents = settings['description']
    contents = re.sub('\[\/\/\]: # \(Goals Table\).*\[\/\/\]: # \(End Goals Table\)',goals,contents,flags=re.DOTALL)
    contents = re.sub('\[\/\/\]: # \(Assists Table\).*\[\/\/\]: # \(End Assists Table\)',assists,contents,flags=re.DOTALL)
    r.subreddit(subreddit).mod.update(description=contents)



updateGoals()
<<<<<<< HEAD
print(getTimestamp() + "Goals Table Updated")
print(getTimestamp() + "Assists Table Updated")
=======
print getTimestamp() + "Goals Table Updated"
print getTimestamp() + "Assists Table Updated"
>>>>>>> 61e6abb36adb514e96c35aae000e0c759b797321


