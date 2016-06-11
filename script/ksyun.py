
#!/usr/bin/python
# coding:utf-8

import requests
import json
from lxml import html

url = "http://www.ksyun.com/user/login?callback=http%3A%2F%2Fwww.ksyun.com"
result = session_requests.get(url)

tree = html.fromstring(result.text)
#authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

result = session_requests.post(
    url, 
    data = payload, 
    headers = dict(referer=url)
)
print result

