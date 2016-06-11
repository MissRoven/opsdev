
#!/usr/bin/python
# coding:utf-8

import requests
import json
from zabbix_client import ZabbixServerProxy
s = ZabbixServerProxy('http://192.168.99.14/zabbix/')
s.user.login(user='Admin', password='zabbix')
data= [        
        {"ip":"172.10.31.12", "host": "yz-ms-web-01"},
        {"ip":"172.10.31.13", "host": "yz-ms-web-02"},
        {"ip":"172.10.31.14", "host": "yz-ms-web-03"},
        {"ip":"172.10.31.15", "host": "yz-ms-web-04"},
        {"ip":"172.10.31.16", "host": "yz-ms-web-05"}
]

interfaces= {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "",
                "dns": "",
                "port": "10050"
            }
groups={
         "groupid": "8"
          }
templates={
                "templateid": "10001"
            }
for i in data:
    interfaces["ip"]=i["ip"]
    s.host.create(host=i["host"],interfaces=interfaces,groups=groups,templates=templates)


