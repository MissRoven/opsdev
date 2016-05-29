#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import  render_template, request
from . import  main
import app.utils
import json
"""
IDC 列表页面
"""
@main.route("/resources/idc/", methods=["GET"])
def resources_idc():
    ret = app.utils.api_action("idc.get")
    return render_template("resources/server_idc_list.html",
                           title="IDC信息",
                           show_resource=True,
                           show=True,
                           idcs=ret)
"""
   修改IDC信息
"""
@main.route("/resources/idc/modify/<int:idc_id>", methods=["GET"])
def resources_idc_modify(idc_id):
    ret = app.utils.api_action("idc.get", {"where":{"id": idc_id,"status":1}})
    if ret:
        return render_template("resources/server_idc_modify.html",
                           title="修改IDC信息",
                           show_resource=True,
                           show=True,
                           idc=ret[0])
    return render_template("404.html"), 404
@main.route("/resources/idc/update",methods=["POST"])
def resources_idc_update():
    data = request.form.to_dict()
    print data
    id = data.pop("id")
    ret = app.utils.api_action("idc.update",{"data": data, "where":{"id":id}})
    if ret:
        return render_template("public/success.html",next_url="/resources/idc/")
    else:
        return render_template("public/error.html", next_url="/resources/idc/")

@main.route("/resources/idc/add/", methods=["GET"])
def resources_add_idc():
        return render_template("resources/server_add_idc.html",
                           title="添加IDC信息")

@main.route("/resources/idc/doadd/", methods=["POST"])
def rescourse_doadd_idc():
    data = request.form.to_dict()

    ret = app.utils.api_action("idc.create",data)
    if ret:
        return render_template("public/success.html",next_url="/resources/idc/")
    else:
        return render_template("public/error.html", next_url="/resources/idc/")

@main.route("/resources/idc/delete/", methods=["POST"])
def resources_delete_idc():
    id = request.form.get("id", 0)
    ret = app.utils.api_action("idc.update", {"where":{"id": id}, "data":{"status": 0}})
    return str(ret)

"""
服务器列表页
"""
@main.route("/resources/server/list/", methods=["GET"])
def resources_server_list():
    return render_template("resources/server_list.html",
                           title="服务器信息",
                           show_resource=True,
                           show=True)

@main.route("/resources/server/add/", methods=["GET"])
def resources_server_add():
    #获取制造商信息
    manufacturers = app.utils.api_action("manufacturers.get")
    #获取业务线信息
    products = app.utils.api_action("product.get", {"where": {"pid": 0}})
    #获取服务器状态信息
    status  = app.utils.api_action("status.get")
    #获取idc信息
    idc_info = app.utils.api_action("idc.get",{"output":['name','id']})
    #raid卡信息
    raids = app.utils.api_action("raid.get")
    #raid卡型号
    #raidtypes = app.utils.api_action("raidtype.get")
    #获取远程管理卡型号
    #managementcardtypes = app.utils.api_action("managementcardtype.get")
    #获取电源功率
    #powers = app.utils.api_action("power.get")
    #供应商信息
    #suppliers = app.utils.api_action("supplier.get")
    return render_template("resources/server_add.html",
                           title="添加服务器",
                           show_resource=True,
                           show=True,
                           manufacturers=manufacturers,
                           products=products,
                           status=status,
                           idc_info=idc_info,
                           raids=raids)


@main.route("/resources/server/manufacturers/add/", methods=["GET"])
def resources_server_manufacturers_add():
    return render_template("resources/server_add_manufacturers.html",
                           title="添加制造商",
                           show_resource=True,
                           show=True)

@main.route("/resources/server/manufacturers/doadd/", methods=["POST"])
def resources_server_manufacturers_doadd():
    params = request.form.to_dict()

    ret = app.utils.api_action("manufacturers.create", params)
    if ret:
        return render_template("public/success.html", next_url="/resources/server/manufacturers/add/")
    else:
        return render_template("public/error.html", next_url="/resources/server/manufacturers/add/")

@main.route("/resources/server_servertype_add/", methods=["GET"])
def resources_server_servertype_add():
    manufacturers = app.utils.api_action("manufacturers.get")
    return render_template("resources/server_add_servertype.html",
                           title="添加服务器型号",
                           show_resource=True,
                           show=True,
                           manufacturers=manufacturers)

@main.route("/resources/server_servertype_doadd/", methods=["POST"])
def resources_server_servertype_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("servertype.create", params)
    jump_url = "/resources/server/manufacturers/add/"
    return app.utils.jump(ret,jump_url,jump_url)


@main.route("/resources/server_product_add/", methods=["GET"])
def resources_server_server_product_add():
    products = app.utils.api_action("product.get",{"where":{"pid":0}})
    print 1232
    print products
    return render_template("resources/server_add_product.html",
                           title="添加业务线",
                           show_resource=True,
                           show=True,
                           products=products)

@main.route("/resources/server_product_doadd/", methods=["POST"])
def resources_server_product_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("product.create", params)
    jump_url = "/resources/server_product_add"
    return app.utils.jump(ret,jump_url,jump_url)




@main.route("/resources/ajax/get_server_type/", methods=["GET"])
def resources_ajax_get_server_type():
    params = request.args.to_dict()
    print params
    if params:
        servertypes = app.utils.api_action("servertype.get",{"where": params})
        return json.dumps(servertypes)
    return ""

@main.route("/resources/ajax/get_server_product/", methods=["GET"])
def resources_ajax_get_product():
    params = request.args.to_dict()
    if params:
        servertypes = app.utils.api_action("product.get",{"output":["id","service_name","pid"],"where":params})
        return json.dumps(servertypes)
    return ""





