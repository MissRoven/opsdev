#  -*- coding: utf-8 -*-
# !/usr/bin/python

import urllib2
import urllib
import cookielib
import re

auth_url = 'http://www.ksyun.com/user/login?callback=http%3A%2F%2Fwww.ksyun.com'
home_url = 'http://console.ksyun.com/';
# 登陆用户名和密码
data={
	"username":"huangxin@kingsoft.com",
	"password":"Ksc1231"
}
# urllib进行编码
post_data=urllib.urlencode(data)
# 发送头信息
headers ={
	"Host":"www.ksyun.com", 
	"Referer": "http://www.ksyun.com"
}
# 初始化一个CookieJar来处理Cookie
cookieJar=cookielib.CookieJar()
# 实例化一个全局opener
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
# 获取cookie
req=urllib2.Request(auth_url,post_data,headers)
print req
result = opener.open(req)
# 访问主页 自动带着cookie信息
result = opener.open(home_url)
# 显示结果
print result.read()

