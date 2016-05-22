#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
import json
from flask import  request,current_app
from . import main

from app.base import JsonRpc



@main.route('/', methods=['GET','POST'])
def index():
    current_app.logger.debug("首页访问日志")
    return 'index'

@main.route('/api', methods=['GET','POST'])
def api():
    #application/json
    #application/json-rpc
    allowed_content = ["application/json","application/json-rpc"]
    #print allowed_content.get(request.content_type, None)

    if request.content_type in allowed_content:
        jsonData = request.get_json()
        jsonrpc = JsonRpc()
        jsonrpc.jsonData = jsonData
        ret = jsonrpc.execute()
        return json.dumps(ret, ensure_ascii=False)
    else:
        current_app.logger.debug('用户请求的content_type为 {}，不予处理'.format(request.content_type))
        return "200", 400
