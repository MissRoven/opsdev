#!/usr/local/bin/python
# coding:utf-8
import os
import imp
import json

from flask import current_app


class AutoLoad():
    """
    自动加载模块
    """
    def __init__(self):
        #指定项目自动加载模块目录
        self.modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules"))
        print self.modules_dir
        current_app.logger.debug("自动加载模块的目录为：{}".format(self.modules_dir))
        self.module_name = ""  #模块名字
        self.func = ""         #函数名字
        self.modules = None    #已加载的模块

    def isValidModule(self, module_name):
        """
        验证模块是否可用
        Args:
            module_name:

        Returns: True/False
        """
        current_app.logger.debug("验证模块是否可用，模块名为：{}".format(module_name))
        self.module_name  = module_name
        return self._load_module()

    def isValidMethod(self, func):
        """
        验证函数是否可用
        Args:
            func:   函数名
        Returns: True/False
        """
        self.func = func
        current_app.logger.debug("验证模块{}，是否存在{}这个属性".format(self.module_name,self.func))
        if self.module is None:
            current_app.logger.warning("函数验证失败，没有验证模块")
            return False
        return hasattr(self.module, self.func)

    def getCallMethod(self):
        """
        返回课执行的函数
        Returns: func

        """
        current_app.logger.debug("获取可以执行的函数")
        if hasattr(self.module, self.func):
            return getattr(self.module, self.func, None)
        return None

    def _load_module(self):
        """
        动态加载模块
        ：return:
        """
        current_app.logger.debug("加载 {} 模块".format(self.module_name))
        ret = False
        #列出模块目录下的所有文件
        for file_name in os.listdir(self.modules_dir):
            #遍历模块目录下的所有文件

            if file_name.endswith(".py"):
                #如果文件名是以.py结尾
                module_name  = file_name.rstrip(".py")   #从文件名中取出模块名

                if module_name  != self.module_name:
                #当前遍历的这个py文件，不是我们想要导入的py文件
                    continue
                fp, pathname, desc = imp.find_module(module_name, [self.modules_dir])
                print fp
                if not fp:
                    continue
                try:
                    self.module = imp.load_module(module_name, fp, pathname, desc)
                    ret = True
                    current_app.logger.debug("加载 {} 模块成功".format(self.module_name))
                except Exception, e:
                    current_app.logger.debug("加载 {} 模块失败".format(self.module_name))
                finally:
                    fp.close()
                    return ret
                break
        return ret

class Response():
    def __init__(self):
        self.data = None                      #待返回的数据
        self.errorCode = 0                    #执行过程中的错误码
        self.errorMessage = None              #执行过程中的错误信息

class JsonRpc():
    def __init__(self):
        self.jsonData = None
        self.VERSION = "2.0"
        self._response = {}      #返回的结果

    def execute(self):
        if self.jsonData.get("id", None) is None:
            self.jsonError(-1, 100, '没有id')
            current_app.logger.error("请求的参数没有id，或者id为None")
            return self._response

        if self.validata():
            #验证通过
            current_app.logger.debug("验证json格式成功")
            params = self.jsonData['params']
            auth = self.jsonData["auth"]
            module, func = self.jsonData['method'].split(".")
            ret = self.callMethod(module,func,params,auth)
            self.processResult(ret)

        return  self._response

    def validata(self):
        """
        验证json数据模式
        Returns:
        """
        if self.jsonData is None:
            self.jsonError(-1, 101, "没有指定json数据")
            current_app.logger.warning("没有传json数据")
            return  False
        #验证是否有指定的属性，一共有5个， jsonrpc,method, id auth, params
        #jsonrpc的值2.0
        #method必须有“.”,切使用点分隔的只有两个元素，不能为空
        #id要是数字
        #auth必须要有，可以为None
        #params 必须为dict，dict可以为空
        fom = ["jsonrpc", "method", "auth", "params"]
        for i in fom:
            if i not in self.jsonData.keys():
                self.jsonError(-1, 102 , '没有 %s 属性'% i)
                current_app.logger.warning("请求的参数中， {} 没有传".format(i))
                return False

        jsondata = self.jsonData
        if jsondata["jsonrpc"] != "2.0":
            self.jsonError(-1, 107, "jsonrpc版本不是正确，应该为{}".format(self.VERSION))
            return False
        jsonmethod = jsondata["method"].split('.')
        if len(jsonmethod) != 2:
            self.jsonError(-1, 108, "method 错误,应该为点分隔的两个字符串")
            return False
        if not jsonmethod[0] or not jsonmethod[1]:
            self.jsonError(-1, 108, "method 错误,应该为点分隔的两个字符串，且不为空")
            return False
        if not str(jsondata["id"]).isdigit():
            self.jsonError(-1, 109, "jsonrpc id  不是数字")
            return False
        if not isinstance(jsondata["params"], dict):
            self.jsonError(-1, 110, "jsonrpc params  必须是字典")
            return False
        return True


    def jsonError(self, id, errno,errmsg):
        """
        处理错误信息
        Args:
            id:
            errno:
            errmsg:
        Returns:
        """
        current_app.logger.debug("处理错误信息")
        self._response = {
            "jsonrpc": self.VERSION,
            "id": id,
            "error_code":errno,
            "errmsg": errmsg
        }
    def requireAuthentication(self, module, func):
        """
        不需要登陆页可以直接访问的白名单列表
        Args:
            module:
            func:
        Returns:  True/False
        """
        b_list = ["user.login", "api.info", "reboot.test", "idc.create"]
        #if "{}.{}".format(module, func) in b_list:
        if True:
            return False
        return False
    def callMethod(self, module, func, params, auth):
        """
        执行apy调用
        Args:
            module:
            func:
            params:
            auth:

        Returns:

        """
        module_name = module.lower()
        func_name = func.lower()

        response = Response()
        at = AutoLoad()

        if not at.isValidModule(module_name):
            current_app.logger.warning("模块导入失败".format(module_name))
            response.errorCode = 120
            response.errorMessage = "模块不存在"
            return response
        if not at.isValidMethod(func_name):
            current_app.logger.warning("函数验证失败".format(func_name))
            response.errorCode = 121
            response.errorMessage = "{} 模块下没有{}这个方法".format(module_name, func_name)
            return response
        if self.requireAuthentication(module_name, func_name):
            #需要登录/需要验证
            if auth is None:
                current_app.logger.warning("{},{} 改操作需要提供token".format(module_name,func_name))
                response.errorCode = 122
                response.errorMessage = "该操作需要提供auth"
                return response
        try:
            called = at.getCallMethod()
            if callable(called):
                response.data = called(**params)
            else:
                current_app.logger.warning("{},{} 不能被调用".format(module_name,func_name))
                response.errorCode = 123
                response.errorMessage = "{}下的{}不能执行"
        except Exception, e:
            response.errorCode = -1
            response.errorMessage = e.message
        return response


    def processResult(self,response):
        """
        处理返回结果
        Args:
            response:

        Returns:
        """
        current_app.logger.debug("处理执行后的结果")
        if response.errorCode != 0:
            self.jsonError(self.jsonData['id'],
                          response.errorCode,
                          response.errorMessage)
        else:
            self._response = {
                "jsonrpc": self.VERSION,
                "result": response.data,
                "id": self.jsonData['id']
            }


if __name__ == "__main__":
    jr = JsonRpc()
    jr.jsonData = {
        "jsonrpc": "2.0",
        "method": "reboot.test",
        "id": 0,
        "auth": None,
        "params": {
            "name": "luo",
            "age": 26
        }
    }
    ret = jr.execute()
    print json.dumps(ret, encoding="UTF-8", ensure_ascii=False)














