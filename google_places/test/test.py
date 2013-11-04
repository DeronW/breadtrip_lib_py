#coding: utf-8
from google_places.api import GooglePlaces

import logging as logger
logger.basicConfig(level=logger.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s")

proxies = {
#    "https": "socks5://127.0.0.1:7070",
#    "https": "https://189.113.64.122:8080",
}

test_api_key = 'AIzaSyDuX29RScH_HjTlvyDGtjXRMqiaTlqn-rc'

api = GooglePlaces(test_api_key)
print api.nearby_search(39.45825, -0.3656816, language='zh_CN', proxies=proxies)

