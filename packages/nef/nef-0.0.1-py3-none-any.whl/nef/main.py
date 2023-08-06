#!/usr/bin/env python

"""command line cloudwatch client"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import subprocess
import json
import os
import re
import datetime
import time
import pkg_resources
from stringcolor import cs, bold, underline

def load_dirty_json(dirty_json):
    """do some crazy shit to the message"""
    regex_replace = [(r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json

def mapFunc(x):
    """reformatting list of timestamps and messages"""
    x['timestamp'] = datetime.datetime.fromtimestamp(x['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')
    x['ingestionTime'] = datetime.datetime.fromtimestamp(x['ingestionTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
    try:
        x['message'] = load_dirty_json(x['message'])
        #x['message'] = json.dumps(x['message'], indent=4, sort_keys=True)
    except:
        x['message'] = x['message']
    return x

def time_to_epoch(str_time):
    """convert yyyy-mm-dd hh:mm:ss to unix epoch"""
    # check for time and seconds parts
    first_split = str_time.split(" ")
    if len(first_split) < 2:
        # there is no time part
        str_time = str_time+" 00:00:00"
        first_split = str_time.split(" ")
    second_split = first_split[1].split(":")
    if len(second_split) < 3:
        # there are no seconds
        str_time = str_time+":00"
    print(str_time)
    print()

    time_tuple = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    time_epoch = time.mktime(time_tuple)
    return str(int(time_epoch) * 1000)

def columnify(iterable):
    """convert iterable to columns"""
    # First convert everything to its repr
    strings = [str(x) for x in iterable]
    # Now pad all the strings to match the widest
    widest = max(len(x) for x in strings)
    padded = [x.ljust(widest) for x in strings]
    return padded

def colprint(iterable, width=72):
    """print iterable in columns"""
    columns = columnify(iterable)
    colwidth = len(columns[0])+2
    perline = (width-4) // colwidth
    for i, column in enumerate(columns):
        print(column, end=' ')
        if i % perline == perline-1:
            print('\n', end='')

def main():
    """cli cloudwatch client"""
    version = pkg_resources.require("nef")[0].version
    parser = argparse.ArgumentParser(
        description='command line cloudwatch client',
        prog='nef',
        formatter_class=rawtxt
    )
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
    parser.add_argument('log', nargs="?", help='Which log group to view')
    parser.add_argument("--start", help="""optional. give a start date and time.
"""+str(cs("format: YYYY-MM-DD HH:MM:SS", "lightgrey13"))+"""
"""+str(cs("example: ", "pink"))+"""nef /path/to/log-group --start 2019-11-25
"""+str(cs("example 2: ", "pink"))+"""nef /path/to/log-group --start \"2019-11-25 10:24\"
"""+str(cs("example 3: ", "pink"))+"""nef /path/to/log-group --start \"2019-11-25 10:24:32\"
"""+str(cs("default (if arg not given): "+yesterday.strftime("%Y-%m-%d %H:%M:%S"), "lightgrey13")), default=yesterday.strftime("%Y-%m-%d %H:%M:%S"))
    args = parser.parse_args()
    log_group = args.log
    start_time = args.start
    if log_group is None:
        print(cs("no log group given", "gold"))
        print(cs("printing a list of log groups:", "DeepSkyBlue2"))
        print()
        describe = "aws logs describe-log-groups --output json"
        log_groups = subprocess.check_output(describe, shell=True).decode("utf-8").strip()
        log_groups = json.loads(log_groups)
        log_groups = log_groups["logGroups"]
        cleansed = []
        if log_groups:
            for lg in log_groups:
                cleansed.append(lg["logGroupName"])
        if cleansed:
            rows, columns = os.popen('stty size', 'r').read().split()
            print(colprint(cleansed, int(columns)))
        else:
            print(cs("sorry,", "red"), cs("could not get a list of log groups", "yellow"))
        exit()
    # setting default start time to yesterday (24 hours ago)
    out = subprocess.check_output("aws logs filter-log-events --log-group-name "+log_group+" --start-time "+time_to_epoch(start_time)+"  --output json", shell=True).decode("utf-8").strip()
    out = json.loads(out)
    out = list(map(mapFunc, out['events']))

    print(json.dumps(out, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
