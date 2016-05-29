#!/usr/bin/python
# coding:utf-8

from flask import current_app
from app.models import ServerType,db

def create(**kwargs):
    # 1  获取用户传入参数
    print kwargs
    # 2  验证参数的合法性
    for field in kwargs.keys():
        if not hasattr(ServerType,field):
            current_app.logger.warning("参数错误，{},不再Servertype这张表中".format(field))
            raise Exception("params error: {}".format(field))
        if not kwargs.get(field,None):
            current_app.logger.warning("参数错误，{},不能为空".format(field))
            raise Exception("{} 不能为空".format(field))
    # 3  插入到数据库
    idc = ServerType(**kwargs)
    db.session.add(idc)

    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")
    # 4  返回插入的状态
    return idc.id

def get(**kwargs):
    # 1. 整理条件
    output = kwargs.get("output",[])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by","id desc")
    where = kwargs.get("where",{})

    # 2. 验证
    # 3. 验证output
    if not isinstance(output, list):
        current_app.logger.warning("output必须为list")
        raise Exception("output必须为list")
    for field in output:
        if not hasattr(ServerType, field):
            current_app.logger.warning("{}这个输出的字段不存在".format(field))
            raise Exception("{}这个输出的字段不存在".format(field))

    # 4. 验证order_by
    tmp_order_by = order_by.split()
    if len(tmp_order_by) != 2:
        current_app.logger.warning("order_by 参数不正确")
        raise Exception("order_by 参数不正确")
    order_by_list = ['desc', 'asc']
    if tmp_order_by[1].lower() not in order_by_list:
        current_app.logger.warning("排序参数不正确，值可以为：{}".format(order_by_list))
        raise Exception("排序参数不正确，值可以为：{}".format(order_by_list))
    if not hasattr(ServerType, tmp_order_by[0].lower()):
        current_app.logger.warning("排序字段不在表中")
        raise Exception("排序字段不在表中")
    # 5. 验证limit
    if not str(limit).isdigit():
        current_app.logger.warning("limit的值必须为数字")
        raise Exception("limit的值必须为数字")

    #查询
    print tmp_order_by
    print tmp_order_by[0]
    print ServerType()
    print getattr(ServerType,tmp_order_by[0])
    print getattr(getattr(ServerType,tmp_order_by[0]), tmp_order_by[1])()
    data = db.session.query(ServerType).filter_by(**where).order_by(getattr(getattr(ServerType,tmp_order_by[0]), tmp_order_by[1])()).limit(limit).all()
    db.session.close()
    ret = []
    for obj in data:

        if output:
            tmp = {}
            for f in output:
                tmp[f] = getattr(obj,f)
            ret.append(tmp)
        else:
            tmp = obj.__dict__
            tmp.pop("_sa_instance_state")
            ret.append(tmp)
    return  ret



def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})

    if not data:
        raise Exception("没有需要更新的")

    for field in data.keys():
        if not hasattr(ServerType, field):
            raise Exception("需要更新的{}这个字段不存在".format(field))

    if not where:
        raise Exception("需要提供where条件")
    if not where.get("id", None):
        raise Exception("需要提供ID作为更新条件")
    if str(where.get("id")).isdigit():
        if int(where.get("id")) <= 0:
            raise Exception("id的值为大于0的整数")
    else:
            raise Exception("条件中的id必须为数字")
    ret = db.session.query(ServerType).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error:{}".format(e.message))
        raise Exception("commit error")
    return ret

def delete(**kwargs):
    where = kwargs.get("where", {})

    if not where:
        raise Exception("需要提供where条件")
    if not where.get("id", None):
        raise Exception("需要提供ID作为更新条件")
    if str(where.get("id")).isdigit():
        if int(where.get("id")) <= 0:
            raise Exception("id的值为大于0的整数")
    else:
        raise Exception("条件中的id必须为数字")
    ret = db.session.query(ServerType).filter_by(**where).delete()
    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error:{}".format(e.message))
        raise Exception("commit error")
    return ret

