from flask import Flask,url_for,render_template  # 引入Flask类 ,url_for反向解析 
from faker import Factory   # 使用faker生成测试数据
app = Flask(__name__)     # 实例化

# ******************  项目测试数据 ****************************
# 使用faker生成
fake = Factory.create()
#fake = Factory.create('zh_CN')   本地化
name = "author name"
movies = []
for i in range(10):
    item = {}
    item["title"] = fake.name()
    item["year"] = fake.year()
    movies.append(item)

# ******************　路由与响应函数 *******************************
'''
@app.route接收 url规则
常规 /xxx
带变量  /<xxx>           
''' 
@app.route("/") 
def index():
    #return "<h1>welcome to my watchlist!</h1><img src='http://helloflask.com/totoro.gif'>"
    return render_template("index.html",name=name,movies=movies)

# 带变量的URL规则
@app.route("/user/<name>")
def user(name):  #变量作参数传入响应函数
    return  "user name : %s" % name

#多个路由可对应一个响应函数
@app.route("/login")
#@app.route("/login1")
#@app.route("/login2")
def login():
    return " login page"

# url_for方法可以通过响应函数名称来反向得到URL地址
@app.route("/url_for")
def test_url_for():
    print(url_for("hello"))     # 不带参数URL
    print(url_for("user",name="guof"))  # 带参数URL
    return "ok"


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
