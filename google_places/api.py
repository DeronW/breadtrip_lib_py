#coding: utf-8
"""
Google places api helper
"""
import requests

import logging as logger
from .constants import POI_TYPE_RESTAURANT, POI_TYPE_MALL, POI_TYPE_HOTEL, POI_TYPE_SIGHTS, \
                       POI_TYPE_UNKNOWN

NEARBY_SEARCH_BASE_URL = "https://maps.googleapis.com/maps/api/place/search/json"
TIMEOUT = 10

def str_bool(b):
    return str(b).lower()

def convert_types(types):
    for t in types:
        if t in ('travel_aency', 'art_gallery', 'museum', 'church', 'place_of_worship'):
            return True, POI_TYPE_SIGHTS
        elif t in ('lodging', ):
            return True, POI_TYPE_HOTEL
        elif t in ('store', 'convenience_store', 'shopping_mall', 'grocery_or_supermarket'):
            return True, POI_TYPE_MALL
        elif t in ('cafe', 'food', 'bar', 'restaurant'):
            return True, POI_TYPE_RESTAURANT
    return False, POI_TYPE_UNKNOWN

class GooglePlaces(object):
    """
    Google places api
    """
    def __init__(self, key):
        self.key = key

    def nearby_search(self, latitude, longitude, proxies={}, **kwargs):
        """
        Nearby search, see also: https://developers.google.com/places/documentation/search#PlaceSearchRequests
        """
        params = dict(latitude=None, longtitude=None, radius=1000, sensor=False, keyword=None,
                      language='en_US', name=None, rankby='prominence', types=None, pagetoken=None)
        params.update(kwargs,location="%s,%s" % (latitude, longitude), key=self.key)
        params["sensor"] = str_bool(params["sensor"])
        params = dict((k, v) for k, v in params.iteritems() if v is not None)
     
        logger.debug('Requesting google service...')
        r = requests.get(NEARBY_SEARCH_BASE_URL, params=params, proxies=proxies, timeout=TIMEOUT)
        ret = r.json
        next_page_token = None
        results = []
        if not ret:
            raise Exception("Google places error")

        if ret["status"] == "OK":
            next_page_token = ret.get("next_page_token")
            results = ret.get('results', [])
        return {
            "next_page_token": next_page_token,
            "items": results,
        }

