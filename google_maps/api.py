#coding: utf-8
"""
Google places api helper
"""
import requests
import logging as logger

from constants import GOOGLE_DOMAIN

GEOCODING_URL = "http://%s/maps/api/geocode/json" % GOOGLE_DOMAIN
TIMEOUT = 10

def str_bool(b):
    return str(b).lower()

class GoogleMapsApi(object):
    """
    Google maps api
    """
    def __init__(self):
        self.proxies = {}

    def geocoding(self, address=None, latitude=None, longitude=None, components=None, sensor=False, 
                        language='en_US'):
        """
        Google geocoding api(See also: https://developers.google.com/maps/documentation/geocoding/)
        
        Args:
        ~~~~~

        - adderss, String, The address that you want to geocode. 
        - latitude, Float
        - longitude, Float
        - components, like [('country', 'CN'), ('administrative_area': 'Helsinki')]
        - sendor, boolean
        - language, String, such as 'en_US', 'zh_CN'

        Optional:

        - language
        
        Returns:
        ~~~~~~~~

        JSON object
        
        Raises:
        ~~~~~~~

        ValueError, Either address or latlon should be provided
        
        """
        components = '|'.join([':'.join(x) for x in (components or [])])

        params = dict(sensor=sensor, language=language)
        if latitude and longitude:
            params.update(latlng='%s,%s' % (latitude, longitude))
        elif address:
            params.update(address=address, components=components)
        elif components:
            params.update(components=components)
        else:
            raise ValueError('Either address or latlon should be provided')

        params["sensor"] = str_bool(params["sensor"])
        logger.debug('Requesting google service...')
        r = requests.get(GEOCODING_URL, params=params, proxies=self.proxies, timeout=TIMEOUT)

        ret = r.json
        results = []
        if not ret:
            raise Exception("Google pai error")

        if ret["status"] == "OK":
            results = ret.get('results', [])
        return {
            "items": results,
        }

