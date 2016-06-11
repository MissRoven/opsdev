#!/usr/bin/python
# coding:utf-8

from flask import current_app
from app.models import Server,db
from app.utils import check_field_exists,check_output_field,check_order_by,check_limit,process_result,check_update_params

def create(**kwargs):
    # 1  获取用户传入参数
    print kwargs
    # 2  验证参数的合法性
    check_field_exists(Server, kwargs, field_none=False)
    # 3  插入到数据库
    idc = Server(**kwargs)
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
    print where

    # 2. 验证
    # 3. 验证output
    check_output_field(Server, output)

    # 4. 验证order_by
    tmp_order_by = check_order_by(Server,order_by)
    # 5. 验证limit
    check_limit(limit)


    #查询
    data = db.session.query(Server).filter_by(**where).order_by(getattr(getattr(Server,tmp_order_by[0]), tmp_order_by[1])()).limit(limit).all()
    db.session.close()
    return process_result(data,output)


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})
    check_update_params(Server, data, where)

    ret = db.session.query(Server).filter_by(**where).update(data)
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
    ret = db.session.query(Server).filter_by(**where).delete()
    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error:{}".format(e.message))
        raise Exception("commit error")
    return ret
