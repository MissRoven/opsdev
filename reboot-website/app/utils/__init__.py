#!/usr/bin/python
# coding:utf-8
from flask import current_app
from app.base import AutoLoad
from flask import  render_template, request

import requests

def api_action(method="", params={}):
    try:
        module, func = method.split(".")
    except ValueError,e:
        current_app.logger.warning("method传值错误：{}".format(e.message))
        return False
    at = AutoLoad()

    if not at.isValidModule(module):
        current_app.logger.warning("{} 模块不可用".format(module))
        return False

    if not at.isValidMethod(func):
        current_app.logger.warning("{} 函数不可用".format(func))
        return False

    try:
        called = at.getCallMethod()
        if callable(called):
            return called(**params)
        else:
            current_app.logger.warning("{}.{} 函数不能被调用".format(module,func))
            return False
    except Exception, e:
        current_app.logger.warning("调用模块执行中出错：{}".format(e.message))
    return False


def apiaction(method="", params={}):
    url = "http://127.0.0.1:9090/api"
    data = {
        "jsonrpc": 2.0,
        "method": method,
        "id": 0,
        "auth": None,
        "params": params
    }
    r = requests.post()


def check_field_exists(obj, data, field_none=[]):

    for field in data.keys():
        if not hasattr(obj,field):
            current_app.logger.warning("参数错误，{},不再idc这张表中".format(field))
            raise Exception("params error: {}".format(field))
        if not data.get(field,None):
            if field_none == False:
                continue
            if field not in field_none:
                current_app.logger.warning("参数错误，{},不能为空".format(field))
                raise Exception("{} 不能为空".format(field))

def check_output_field(obj, output):
    if not isinstance(output, list):
        current_app.logger.warning("output必须为list")
        raise Exception("output必须为list")
    for field in output:
        if not hasattr(obj, field):
            current_app.logger.warning("{}这个输出的字段不存在".format(field))
            raise Exception("{}这个输出的字段不存在".format(field))

def check_order_by(obj, order_by):
    tmp_order_by = order_by.split()
    if len(tmp_order_by) != 2:
        current_app.logger.warning("order_by 参数不正确")
        raise Exception("order_by 参数不正确")
    order_by_list = ['desc', 'asc']
    if tmp_order_by[1].lower() not in order_by_list:
        current_app.logger.warning("排序参数不正确，值可以为：{}".format(order_by_list))
        raise Exception("排序参数不正确，值可以为：{}".format(order_by_list))
    if not hasattr(obj, tmp_order_by[0].lower()):
        current_app.logger.warning("排序字段不在表中")
        raise Exception("排序字段不在表中")
    return tmp_order_by

def check_limit(limit):
    if not str(limit).isdigit():
        current_app.logger.warning("limit的值必须为数字")
        raise Exception("limit的值必须为数字")

def process_result(data, output):
    ret = []
    for obj in data:

        if output:
            tmp = {}
            for f in output:
                tmp[f] = getattr(obj, f)
            ret.append(tmp)
        else:
            tmp = obj.__dict__
            tmp.pop("_sa_instance_state")
            ret.append(tmp)
    return ret

def check_update_params(obj, data, where):
    if not data:
        raise Exception("没有需要更新的")

    for field in data.keys():
        if not hasattr(obj, field):
            raise Exception("需要更新的{}这个字段不存在".format(field))

    if not where:
        raise Exception("需要提供where条件")
    if not where.get("id", None):
        raise Exception("需要提供ID作为更新条件")
    if str(where.get("id")).isdigit():
        if int(where.get("id")) <= 0:
            raise Exception("id的值为大于0的整数")
        else:
            where = {"id": where.get("id")}
    else:
        raise Exception("条件中的id必须为数字")


def jump(ret,success_url="/", error_url="/"):
    success = "public/success.html"
    error = "public/error.html"
    if ret:
        return render_template(success, next_url=success_url)
    else:
        return render_template(error, next_url=error_url)

class Treeview(object):
    def __init__(self):
        self.product_info = api_action("product.get", {"output": ["id", "module_letter", "pid"]})
        self.idc_info = api_action("idc.get", {"output": ["id", "name"]})
        self.data = []

    def get_child_node(self):
        ret = []
        for p in filter(lambda x: True if x.get("pid", None) == 0 else False, self.product_info):
            node = {}
            node['text'] = p.get("module_letter", None)
            node['id'] = p.get("id", None)
            node["type"] = "service"
            node["nodes"] = self.get_grant_node(p.get("id", None))
            ret.append(node)
        return ret

    def get_grant_node(self, pid):
        ret = []
        for p in filter(lambda x: True if x.get("pid", None) == pid else False, self.product_info):
            node = {}
            node['text'] = p.get("module_letter", None)
            node['id'] = p.get("id", None)
            node["type"] = "product"
            node["pid"] = pid
            ret.append(node)
        return ret

    def get(self, idc=False):
        child = self.get_child_node()
        if not idc:
            return child



