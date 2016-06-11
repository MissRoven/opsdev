
#!/usr/bin/python
# coding:utf-8

import requests
import json

url = "http://192.168.99.14/zabbix/api_jsonrpc.php"

header = {'Content-Type': 'application/json-rpc'}
data = {
    "jsonrpc": "2.0",
    "method": "apiinfo.version",
    "id": 1,
    "auth": None,
    "params": {}
}

r = requests.post(url, data=json.dumps(data), headers=header)
print r.status_code
print r.content


data2 = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "zabbix"
    },
    "id": 1,
    "auth": None
}

rr = requests.post(url, data=json.dumps(data2), headers=header)
print rr.status_code
print rr.content



data3 = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "selectInterfaces": [
            "interfaceid",
            "ip"
        ]
    },
    "id": 2,
    "auth": "3d0a19c47397ac5ba1004dd0b90b6fa2"
}


rr = requests.post(url, data=json.dumps(data3), headers=header)
print rr.status_code
print rr.content



data4 = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": "Free disk space on $1",
        "key_": "vfs.fs.size[/data,free]",
        "hostid": "10106",
        "type": 0,
        "value_type": 3,
        "interfaceid": "3",
        "delay": 30
    },
    "auth": "400bab2d29083244046340dfc64dc63f",
    "id": 3
}


data4 = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "test",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "192.168.99.10",
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
          {
         "groupid": "8"
          }
       ],
         "templates": [
            {
                "templateid": "10001"
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
    },
    "id": 3,
    "auth": "400bab2d29083244046340dfc64dc63f"
}

data99 = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
        "filter": {
            "name": [
                "my-test",
                "Linux servers"
            ]
        }
    },
    "auth": "400bab2d29083244046340dfc64dc63f",
    "id": 1
}

data4 = {
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": "extend",
        "filter": {
            "host": [
                "Template OS Linux",
                "Template OS Windows",
                "Template SNMP OS Linux"
            ]
        }
    },
    "auth": "400bab2d29083244046340dfc64dc63f",
    "id": 1
}
rr = requests.post(url, data=json.dumps(data4), headers=header)
print rr.status_code
print rr.content

