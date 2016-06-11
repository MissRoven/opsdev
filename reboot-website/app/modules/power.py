#!/usr/bin/python
# coding:utf-8

from flask import current_app
from app.models import Power,db
from app.utils import check_field_exists,check_output_field,check_limit,check_order_by,process_result

def create(**kwargs):
    # 1  获取用户传入参数
    print kwargs
    # 2  验证参数的合法性
    check_field_exists(Power, kwargs)
    # 3  插入到数据库
    manufacturers = Power(**kwargs)
    db.session.add(manufacturers)

    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")
    # 4  返回插入的状态
    return manufacturers.id


def get(**kwargs):
    # 1. 整理条件
    output = kwargs.get("output",[])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by","id desc")
    where = kwargs.get("where",{})

    # 2. 验证
    # 3. 验证output
    check_output_field(Power, output)

    # 4. 验证order_by
    tmp_order_by = check_order_by(Power, order_by)
    # 5. 验证limit
    check_limit(limit)

    #查询
    data = db.session.query(Power).filter_by(**where).order_by(getattr(getattr(Power,tmp_order_by[0]), tmp_order_by[1])()).limit(limit).all()
    db.session.close()
    return process_result(data,output)


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})
    check_update_params(Power, data, where)

    ret = db.session.query(Power).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error:{}".format(e.message))
        raise Exception("commit error")
    return ret