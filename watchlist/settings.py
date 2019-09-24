#一般开发写测试需要经常切换debug和测试模式
# app.config['DEBUG']=True      #debug模式，日志级别低，一般在开发环境用，报错直接回在前端页面显示，具体到代码
# app.config['TESTING']=True    #测试模式，日志级别较高，无限接近线上环境，报错只在后端显示具体错误，前端页面之后提示有错，不会具体显示
import os

class DebugMode(object):
    DEBUG = True
    ENV="development"
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'guof@163.com'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'demo'
    #mysql
    #SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    #    DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE
    #)
    #SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingMode(object):
    TESTING = True
    ENV = "production"
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'guof@163.com'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'demo'
 
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True