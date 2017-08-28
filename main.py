#!/usr/local/bin/python
#import os

import subprocess

subprocess.call(['/root/reddit/sidebar/injury/update.py'])
subprocess.call(['/root/reddit/sidebar/results/update.py'])
subprocess.call(['/root/reddit/sidebar/table/update.py'])
subprocess.call(['/root/reddit/sidebar/statistics/update.py'])


