#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import  render_template, request
from . import  main
from app.models import Zbhost,Server,db
import app.utils
import json
from app.base.zabbix import Zabbix,rsync_server_to_zbhost,rsync_zabbix_to_zbhost

"""
IDC 列表页面
"""
@main.route("/resources/idc/", methods=["GET"])
def resources_idc():
    ret = app.utils.api_action("idc.get",{"where":{"status":1}})
    return render_template("resources/server_idc_list.html",
                           title="IDC信息",
                           show_resource=True,
                           show_idc_list=True,
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
                           show_idc_list=True,
                           idc=ret[0])
    return render_template("404.html"), 404

@main.route("/resources/idc/update",methods=["POST"])
def resources_idc_update():
    data = request.form.to_dict()
    print data
    id = data.pop("id")
    ret = app.utils.api_action("idc.update",{"data": data, "where":{"id":id}})
    jump_url = "/resources/idc/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
   添加IDC信息
"""
@main.route("/resources/idc/add/", methods=["GET"])
def resources_add_idc():
        return render_template("resources/server_add_idc.html",
                           title="添加IDC信息",
                           show_resource = True,
                           show_idc_list = True)

@main.route("/resources/idc/doadd/", methods=["POST"])
def rescourse_doadd_idc():
    data = request.form.to_dict()

    ret = app.utils.api_action("idc.create",data)
    jump_url = "/resources/idc/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

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
    servers = app.utils.api_action("server.get")
    print servers
    return render_template("resources/server_list.html",
                           title="服务器信息",
                           show_resource=True,
                           show_serverlist=True,
                           servers=servers)

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
    #获取机会号
    cabinets = app.utils.api_action("cabinets.get")
    #raid卡信息
    raids = app.utils.api_action("raid.get")
    #raid卡型号
    raidtypes = app.utils.api_action("raidtype.get")
    #获取远程管理卡型号
    managementcardtypes = app.utils.api_action("managementcardtype.get")
    #获取电源功率
    powers = app.utils.api_action("power.get")
    #供应商信息
    suppliers = app.utils.api_action("supplier.get")
    return render_template("resources/server_add.html",
                           title="添加服务器",
                           show_resource=True,
                           show_serverlist=True,
                           manufacturers=manufacturers,
                           products=products,
                           status=status,
                           idc_info=idc_info,
                           raids=raids,
                           raidtypes=raidtypes,
                           managementcardtypes=managementcardtypes,
                           powers=powers,
                           suppliers=suppliers,
                           cabinets=cabinets)

@main.route("/resources/server/doadd/", methods=["POST"])
def resources_server_doadd():
    params = request.form.to_dict()
    print params
    ret = app.utils.api_action("server.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
   修改服务器信息
"""
@main.route("/resources/server/modify/<int:server_id>", methods=["GET"])
def resources_server_modify(server_id):
    ret = app.utils.api_action("server.get", {"where":{"id": server_id}})
    print ret
    if ret:
        return render_template("resources/server_modify.html",
                           title="修改SERVER信息",
                           show_resource=True,
                           show=True,
                           server=ret[0])
    return render_template("404.html"), 404

"""
   添加服务器状态
"""
@main.route("/resources/status/add/", methods=["GET"])
def resources_server_status_add():
    return render_template("resources/server_add_status.html",
                           title="添加服务器状态",
                           show_resource=True,
                           show=True)

@main.route("/resources/status/doadd/", methods=["POST"])
def resources_server_status_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("status.create", params)
    jump_url = "/resources/status/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
   添加制造商
"""
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
    jump_url = "/resources/server/manufacturers/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   添加服务器型号
"""
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
    jump_url = "/resources/server_servertype_add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   添加业务线
"""
@main.route("/resources/server_product_add/", methods=["GET"])
def resources_server_server_product_add():
    products = app.utils.api_action("product.get",{"where":{"pid":0}})
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
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
    ajax 操作
    获取服务器型号
"""
@main.route("/resources/ajax/get_server_type/", methods=["GET"])
def resources_ajax_get_server_type():
    params = request.args.to_dict()
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


"""
   添加机柜号
"""

@main.route("/resources/cabinet/add/", methods=["GET"])
def resources_server_cabinet_add():
    idcs = app.utils.api_action("idc.get",{"output":['name','id']})
    powers = app.utils.api_action("power.get")
    return render_template("resources/server_add_cabinet.html",
                           title="添加机柜号",
                           show_resource=True,
                           show=True,
                           idcs=idcs,
                           powers=powers)

@main.route("/resources/cabinet/doadd/", methods=["POST"])
def resources_server_cabinet_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("cabinets.create", params)
    jump_url = "/resources/cabinet/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   添加RAID
"""

@main.route("/resources/server_raid_add/", methods=["GET"])
def resources_server_raid_add():
    return render_template("resources/server_add_raid.html",
                           title="添加RAID",
                           show_resource=True,
                           show=True)

@main.route("/resources/server_raid_doadd/", methods=["POST"])
def resources_server_raid_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("raid.create", params)
    jump_url = "/resources/server_raid_add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   添加RAID型号
"""

@main.route("/resources/server_raidcardtype_add/", methods=["GET"])
def resources_server_raidcardtype_add():
    return render_template("resources/server_add_raidcardtype.html",
                           title="添加RAID型号",
                           show_resource=True,
                           show=True)

@main.route("/resources/server_raidcardtype_doadd/", methods=["POST"])
def resources_server_raidcardtype_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("raidtype.create", params)
    jump_url = "/resources/server_raidcardtype_add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   添加远程管理卡
"""

@main.route("/resources/server_managementcardtype_add/", methods=["GET"])
def resources_server_managementcardtype_add():
    return render_template("resources/server_add_managementcardtype.html",
                           title="添加远程管理卡",
                           show_resource=True,
                           show=True)

@main.route("/resources/server_managementcardtype_doadd/", methods=["POST"])
def resources_server_managementcardtype_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("managementcardtype.create", params)
    jump_url = "/resources/server_managementcardtype_add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   添加电源功率
"""

@main.route("/resources/power/add/", methods=["GET"])
def resources_power_add():
    return render_template("resources/server_add_power.html",
                           title="添加电源功率",
                           show_resource=True,
                           show=True)

@main.route("/resources/power/doadd/", methods=["POST"])
def resources_power_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("power.create", params)
    jump_url = "/resources/power/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
   添加供应商
"""

@main.route("/resources/server_supplier_add/", methods=["GET"])
def resources_server_supplier_add():
    return render_template("resources/server_add_supplier.html",
                           title="添加供应商",
                           show_resource=True,
                           show=True)

@main.route("/resources/server_supplier_doadd/", methods=["POST"])
def resources_server_supplier_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("supplier.create", params)
    jump_url = "/resources/server_supplier_add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
   服务器信息自动上报
"""
@main.route("/resources/server/reporting/", methods=["POST"])
def resources_server_reporting():
    params = request.form.to_dict()
    where = {}
    if params.get("st", None) and len(params['st']) > 3:
        where['st'] = params.pop('st')
    else:
        where['uuid'] = params.pop('uuid')

    host = app.utils.api_action("server.get", {"where": where})
    if host:
        #update
        app.utils.api_action("server.update",{"data": params, "where": {"id": host[0]["id"]}})
    else:
        params.update(where)
        app.utils.api_action("server.create", params)

    return ""

"""
ajax 获取不再zabbix里的主机
"""
@main.route("/resource/monitor/ajax/get_sync_zabbix_hosts", methods=["POST"])
def get_sync_zabbix_hosts():

    #1.取出在zabbix里的所有主机
    zabbix_hosts = db.session.query(Zbhost).all()
    #2 组合条件IP
    host_ips = [zb.ip for zb in zabbix_hosts]
    #3取出不在zabbix里的所有主机（条件： ip（在zabbix里的所有主机ip））
    servers = db.session.query(Server).filter(~Server.inner_ip.in_(host_ips)).all()
    return json.dumps([{"hostname": s.hostname,"id":s.id} for s in servers])

"""
   ajax 操作，同步主机到zabbix
"""
@main.route("/resource/monitor/ajax/sync_host_to_zabbix", methods=["POST"])
def resource_sync_hosts_to_zabbix():
    if  request.method == "POST":
        params = request.form.to_dict()
        hostids = params['hostids'].split(',')
        servers = db.session.query(Server).filter(Server.id.in_(hostids)).all()
        data = {}
        zb = Zabbix()
        flag = True
        for server in servers:
            ret = zb.create_zb_host(server.hostname, server.inner_ip, params['groupid'])
            if isinstance(ret, dict) and ret.get("hostids", None):
                data[server.hostname] = True
            else:
                flag = False
                data[server.hostname] = ret

        rsync_zabbix_to_zbhost()
        rsync_server_to_zbhost()
        if flag:
            return "1"
        else:
            return json.dumps(data)
    return "500"