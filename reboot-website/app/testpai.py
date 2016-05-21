#!/usr/bin/python
# coding:utf-8
import requests
import  json
url = "http://127.0.0.1:9090/api"

def test_api():
    header = {
        "content-type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "reboot.error1",
        "id": 0,
        "auth": None,
        "params": {
            "name": "luo"
        }
    }
    r = requests.post(url, headers=header, data=json.dumps(data))
    print r.status_code
    print r.content


if __name__ == "__main__":
    test_api()
