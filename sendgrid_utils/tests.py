# -*- coding: utf-8 -*-
from smtp_api_header import SmtpApiHeader

hdr = SmtpApiHeader()

for i in range(1000):
    hdr.addTo('piglei2007@gmail.com')
    hdr.addTo('piglei2005@126.com')

hdr.addSubVal('-username-', ['a', 'b'])
hdr.addSubVal('-userid-', [u'测试用户', 'b'])

print hdr.asJSON()
print hdr.as_string()
