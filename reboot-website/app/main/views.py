#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from . import main
from app.base import JsonRpc

import json

from flask import  request





@main.route('/', methods=['GET','POST'])
def index():
    return 'index'

@main.route('/api', methods=['GET','POST'])
def api():
    #application/json
    #application/json-rpc
    allowed_content_list = ["application/json","application/json-rpc"]
    allowed_content = ''
    print allowed_content.get(request.content_type, None)
    return 'ok'
    if allowed_content.get(request.content_type, None) in allowed_content_list:
        jsonData = request.get_json()
        jsonrpc = JsonRpc()
        jsonrpc.jsonData = jsonData
        ret = jsonrpc.execute()
        return json.dumps(ret, ensure_ascii=False)
    else:
        return "200", 400
