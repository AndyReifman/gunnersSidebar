#!/usr/bin/python2.7

import subprocess

subprocess.call(['/root/reddit/sidebar/injury/update.py'])
subprocess.call(['/root/reddit/sidebar/results/update.py'])
subprocess.call(['/root/reddit/sidebar/table/update.py'])
subprocess.call(['/root/reddit/sidebar/statistics/update.py'])


