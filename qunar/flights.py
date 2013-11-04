#coding: utf-8
"""
Fetch flight infos from `qunar.com`
"""
import datetime
import requests
import dateutil.parser
from lxml import etree
from btrip_utils.text import text_wrapped_by

TIMEOUT = 10
FLIGHT_STATUS_QUERY_NATIVE_URL = "http://flight.qunar.com/status/fquery.jsp"
FLIGHT_STATUS_QUERY_GLOBAL_URL = "http://flight.qunar.com/schedule/international/fquery.jsp"

def get_flight_status_by_code(flight_code, departure_date=None):
    """
    Query flight status from qunar
    """
    r = requests.get(FLIGHT_STATUS_QUERY_NATIVE_URL, params={
            "flightCode": flight_code
        }, timeout=TIMEOUT)
    airports = text_wrapped_by('stopInfo.update(', ')', r.text)
    if not airports:
        return

    airports = [ x.strip()[1:-1] for x in airports.strip().split(',') ]

    root = etree.HTML(r.text)
    _date = datetime.date.today() if not departure_date else departure_date
    datetimes = root.xpath('//span[@class="ctime2"]')[1]
    departure_date_local = datetimes.text
    arrival_date_local = datetimes.xpath('em/text()')[0]
    # Processing disgusting "day not given" problem
    # TODO: use a utc date instead, need to get timezone from airport iata code
    departure_date_local =  dateutil.parser.parse('%s %s.000Z' % (_date, departure_date_local))
    arrival_date_local = dateutil.parser.parse('%s %s.000Z' % (_date, arrival_date_local))
    for days in (1, 2):
        if root.xpath('//span[@class="d%s"]' % days):
            arrival_date_local += datetime.timedelta(days=days)

    while departure_date_local > arrival_date_local:
        arrival_date_local += datetime.timedelta(days=1)

    return {
        'departure_airport': airports[0],
        'departure_date_local': departure_date_local.strftime('%Y-%m-%d %H:%M'),
        'arrival_airport':  airports[1],
        'arrival_date_local': arrival_date_local.strftime('%Y-%m-%d %H:%M'),
    }

if __name__ == '__main__':
    print get_flight_status_by_code('PN6226', departure_date=datetime.date(2011, 1, 1))
