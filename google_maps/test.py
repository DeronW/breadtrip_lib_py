# -*- coding: utf-8 -*-
import pprint
from google_maps.api import GoogleMapsApi

class TestGoogleMapsApi(object):
    @classmethod
    def setup_class(cls):
        cls.api = GoogleMapsApi()

    def test_geocoding(self):
        assert len(self.api.geocoding(address='怀化')['items']) != 0
        assert self.api.geocoding(address='北京', language='zh_CN')
        assert self.api.geocoding(address='北京', language='zh_CN', components=(('country', 'US'),))

