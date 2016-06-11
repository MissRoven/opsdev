#!/usr/bin/env python
# coding:utf-8

import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KDY") or "abcdefg"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True     # 每次执行数据库操作时都终端输出
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/reboot"
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s- %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(os.path.join(basedir, 'flask.log'))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        print app.logger.handlers

class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
