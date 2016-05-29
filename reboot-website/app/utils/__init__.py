#!/usr/bin/python
# coding:utf-8
from flask import current_app
from app.base import AutoLoad
from flask import  render_template, request

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


def jump(ret,success_url="/", error_url="/"):

    if ret:
        return render_template("public/success.html", next_url=success_url)
    else:
        return render_template("public/error.html", next_url=error_url)

