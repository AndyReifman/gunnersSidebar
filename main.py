#!/usr/bin/python3

import subprocess
import os

subprocess.call([os.path.join(os.path.dirname(os.path.abspath(__file__)), 'injury/update.py')])
subprocess.call([os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results/update.py')])
subprocess.call([os.path.join(os.path.dirname(os.path.abspath(__file__)), 'table/update.py')])
subprocess.call([os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statistics/update.py')])
