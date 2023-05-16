#!/usr/bin/env python3

"""
CONFIG SCRIPT for the alfred-ICDbrowser Workflow
"""


import os
import sys

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)




DATA_FOLDER = os.getenv('alfred_workflow_data')
DATABASE_FILE = DATA_FOLDER + '/icd.db'

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(DATABASE_FILE):
    os.rename('icd.db', DATABASE_FILE)
