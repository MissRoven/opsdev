#!/usr/bin/python
# coding:utf-8
import requests
import  json
url = "http://127.0.0.1:9090/api"
header = {
    "content-type": "application/json"
}
def test_api():

    data = {
        "jsonrpc": "2.0",
        "method": "idc.create",
        "id": 0,
        "auth": None,
        "params": {
                "name": "YZ",
                "idc_name": "北京亦庄机房",
                "address": "北京亦庄机房",
                "phone": "12345678" ,
                "email": "test@55.com",
                "user_interface": "roven",
                "user_phone": "12132454354",
                "rel_cabinet_num": 50,
                 "pact_cabinet_num": 60,
        }
    }
    r = requests.post(url, headers=header, data=json.dumps(data))
    print r.status_code
    print r.content
def test_get():

    data = {
        "jsonrpc": "2.0",
        "method": "idc.get",
        "id": 0,
        "auth": None,
        "params": {
            "output": ["id"]
        }
    }
    r = requests.post(url, headers=header, data=json.dumps(data))
    print r.status_code
    print r.content

def test_update():

    data = {
        "jsonrpc": "2.0",
        "method": "idc.update",
        "id": 0,
        "auth": None,
        "params": {
            "data": {
                "rel_cabinet_num": 100
            },
            "where": {
                "id": 1
            }
        }
    }
    r = requests.post(url, headers=header, data=json.dumps(data))
    print r.status_code
    print r.content

if __name__ == "__main__":
    test_get()
