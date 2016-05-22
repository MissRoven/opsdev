#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import  render_template, request
from . import  main
import app.utils

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
    ret = app.utils.api_action("idc.get", {"where":{"id": idc_id}})
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

@main.route("/resources/idc/<int:idc_id>", methods=["GET"])
def resources_delete_idc(idc_id):
    ret = app.utils.api_action("idc.delete", {"where":{"id": idc_id}})
    if ret:
        return render_template("public/success.html",next_url="/resources/idc/")
    else:
        return render_template("public/error.html", next_url="/resources/idc/")

