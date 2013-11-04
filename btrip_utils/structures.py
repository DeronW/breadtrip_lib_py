#coding: utf-8
"""
Structures for BreadTrip
"""
import datetime

def date_range(date_start, date_end):
    days = (date_end - date_start).days
    if days > 0:
        for i in range(days):
            yield date_start + datetime.timedelta(days=i)

if __name__ == '__main__':
    for day in date_range(datetime.date(2012, 11, 18), datetime.date(2012, 12, 2)):
        print day
    for day in date_range(datetime.date(2013, 11, 18), datetime.date(2012, 12, 2)):
        print day
