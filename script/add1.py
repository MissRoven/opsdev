
#!/usr/bin/python
# coding:utf-8

import requests
import json
from zabbix_client import ZabbixServerProxy
s = ZabbixServerProxy('http://192.168.99.14/zabbix/')
s.user.login(user='Admin', password='zabbix')
data= [        
        {"ip":"172.10.31.12", "host": "yz-ms-web-11"},
        {"ip":"172.10.31.13", "host": "yz-ms-web-12"},
        {"ip":"172.10.31.14", "host": "yz-ms-web-13"},
        {"ip":"172.10.31.15", "host": "yz-ms-web-14"},
        {"ip":"172.10.31.16", "host": "yz-ms-web-15"}
]

interfaces= {
                "type": 2,
                "main": 1,
                "useip": 1,
                "ip": "",
                "dns": "",
                "port": "161"
            }
groups={
         "groupid": "8"
          }
templates={
                "templateid": "10069"
            }
for i in data:
    interfaces["ip"]=i["ip"]
    s.host.create(host=i["host"],interfaces=interfaces,groups=groups,templates=templates)


