#coding: utf-8
"""
Utils about apilog
"""
import os
import json
import datetime
import dateutil
import dateutil.parser
import logging
from .text import text_wrapped_by

def parse_apilog_line(line, with_time=False, with_extra=False):
    """
    Parse syslog log line
    """
    line = line.strip()
    _api_name, uid, args = line.split('|', 2)
    if '|' in args:
        request_method, args = args.split('|', 1)
    else:
        request_method = 'UNKNOWN'
    try:
        logtime, api_name = _api_name.rsplit(None, 1)
    except:
        return

    try:
        args = args.decode('utf-8', 'ignore')
        info = json.loads(args)
    except:
        info = {}
    ret = {
        'api_name': api_name,
        'request_method': request_method,
        'info': info,
        'user': int(uid) if uid != 'anoy' else None,
    }
    if with_time:
        logtime =  text_wrapped_by('[', ']', logtime)
        try:
            logtime = datetime.datetime.strptime(logtime, '%Y-%m-%d %H:%M:%S,%f')
        except:
            logtime = dateutil.parser.parse(logtime)
        ret.update(time=logtime.replace(tzinfo=None))
    return ret


def parse_activity_log_line(line):
    """
    Parse activity log line
    """
    line = line.strip()
    _api_name, uid, args = line.split('|', 2)
    try:
        logtime, api_name = _api_name.rsplit(None, 1)
    except:
        return
    try:
        args = args.decode('utf-8', 'ignore')
        info = json.loads(args)
    except:
        info = {}
    ret = {
        'activity': api_name,
        'user': int(uid) if uid != 'anoy' else None,
    }
    ret.update(info)

    logtime =  text_wrapped_by('[', ']', logtime)
    try:
        logtime = datetime.datetime.strptime(logtime, '%Y-%m-%d %H:%M:%S,%f')
    except:
        logtime = dateutil.parser.parse(logtime)
    ret.update(date_added=logtime.replace(tzinfo=None))
    return ret


def api_logs_by_day(day, anoymous=False):
    """
    Return parsed api logs
    """
    apilog_file = "/data/logs/breadtrip/syslog/api/%s.log" % day
    if not os.path.exists(apilog_file):
        raise StopIteration
    logging.info("Openning %s..." % apilog_file)
    with open(apilog_file, 'r') as fp:
        for line in fp:
            data = parse_apilog_line(line)
            if not data:
                continue
            if anoymous and not data['user']:
                continue
            yield data

