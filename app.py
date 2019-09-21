from flask import Flask,url_for,render_template  # 引入Flask类 ,url_for反向解析 
from faker import Factory   # 使用faker生成测试数据
from settings import DebugMode,TestingMode  # 设置模式
from flask_sqlalchemy import SQLAlchemy  #  数据库扩展
import os
import sys
import click

app = Flask(__name__)     # 实例化

#***************  数据库扩展********************
# sqlite
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path,"data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)   

# ********************** 开发模式设置 *************************
app.config.from_object(DebugMode)    #开启DEBUG模式，直接在前端页面显示错误代码
#app.config.from_object(TestingMode)  #而在TESTING模式下前端页面之会提示错误，并不会有具体代码


# ************************ 定义模型类 ****************************************class User(db.Model):  
class User(db.Model):
    __tablename__ = "wl_user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    __tablename__ = "wl_movie"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

# *************************   项目测试数据 ******************************
fake = Factory.create()
#fake = Factory.create('zh_CN')   本地化

# 使用click方式生成数据库数据
@app.cli.command()
def gen_db_data():
    users = []
    movies = []
    for i in range(10):
        item = {}
        item["title"] = fake.name()
        item["year"] = fake.year()
        movies.append(item)
    for i in range(5):
        item = {}
        item["name"]=fake.name()
        users.append(item)

    db.session.bulk_insert_mappings(User,users) # 批量插入数据
    db.session.bulk_insert_mappings(Movie,movies)
    db.session.commit()
    click.echo("data generate successfully!")

# ******************　路由与响应函数 *******************************
# 主页
@app.route("/") 
def index():
    #return "<h1>welcome to my watchlist!</h1><img src='http://helloflask.com/totoro.gif'>"
    user = User.query.first()
    movies = Movie.query.all()
    return render_template("index.html",user=user,movies=movies)

# 带变量的URL规则
@app.route("/user/<name>")
def user(name):  #变量作参数传入响应函数
    return  "user name : %s" % name

# url_for方法可以通过响应函数名称来反向得到URL地址
@app.route("/url_for")
def test_url_for():
    print(url_for("hello"))     # 不带参数URL
    print(url_for("user",name="guof"))  # 带参数URL
    return "ok"

# 模板过滤器
@app.template_filter("my_filter")
def gf(value):
    return value.replace('name','guof')

# *************************  flask程序启动 *********************************
'''
# 1 实例启动  app.run()
# 2 命令行启动  flask run  启用flask发现机制,默认启动程序在app.py或wsgi.py中,可通过环境变量FLASK_APP来更该改启动程序
'''
if __name__ == "__main__":
    app.run()
