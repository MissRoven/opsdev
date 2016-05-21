# coding:utf-8
"""
1.所有的结果直接返回
2.error ,try -execpt raise Exception
"""

def test(**kwargs):
    return kwargs
def error(**kwargs):
    raise Exception("执行过程中出现错误")
