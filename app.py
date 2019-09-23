from flask import Flask,url_for,render_template,request,flash,redirect # 引入Flask类 ,url_for反向解析 
from faker import Factory   # 使用faker生成测试数据
from settings import DebugMode,TestingMode  # 设置模式
from flask_sqlalchemy import SQLAlchemy  #  数据库扩展
from werkzeug.security import generate_password_hash,check_password_hash  #密码加密、验证
from flask_login import LoginManager,login_user,UserMixin,login_required, logout_user,current_user  #用户认证
import os
import sys
import click   #命令行工具


# ****************  flask实例化 *******************
app = Flask(__name__)  

#***************  数据库扩展********************
# sqlite,文件型数据库
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path,"data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)    #初始化db对象

# ********************** 开发模式设置 *************************
app.config.from_object(DebugMode)    #开启DEBUG模式，直接在前端页面显示错误代码
#app.config.from_object(TestingMode)  #而在TESTING模式下前端页面之会提示错误，并不会有具体代码


# ***********************用户认证　××××××××××××××××××××××××××××××××××
'''
 Flask-Login 提供了一个 current_user 变量， 注册这个函数的目的是如查用户已登录， 
 current_user 变量的值会是当前用户的用户模型类记录。

另一个步骤是让存储用户的 User 模型类继承 Flask-Login 提供的 UserMixin 类
会让 User 类拥有几个用于判断认证状态的属性和方法
is_authenticated
'''
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

# ************************ 定义模型类 ****************************************class User(db.Model):  
class User(db.Model,UserMixin):                      #继承自db.Model
    __tablename__ = "wl_user"              # 数据库表名，未定义则默认是类名
    id = db.Column(db.Integer,primary_key=True)   # flask中主键必须显示定义，自增长类型
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash =db.Column(db.String(128))
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movie(db.Model):
    __tablename__ = "wl_movie"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

# *************************   项目测试数据 ******************************
fake = Factory.create()     # 通过fake扩展模块来生成测试数据
#fake = Factory.create('zh_CN')   本地化

# 使用click方式生成数据库数据
@app.cli.command()     #命令注册
def gen_db_data():
    db.drop_all()
    db.create_all()
    users = []
    movies = []
    for i in range(10):
        item = {}
        item["title"] = fake.name()
        item["year"] = fake.year()
        movies.append(item)
    for i in range(1):
        item = {}
        item["name"]=fake.name()
        users.append(item)
    db.session.bulk_insert_mappings(User,users) # 批量插入数据
    db.session.bulk_insert_mappings(Movie,movies)
    db.session.commit()
    click.echo("data generated!")

# *************** 生成管理员账户 *******************************
@app.cli.command()
@click.option("--username",prompt=True,help="the username used to login")
@click.option("--password",prompt=True,hide_input=True,confirmation_prompt=True,help="the password used to login")
def admin(username,password):
    user = User.query.first()
    if user is not None:
        click.echo("update user..")
        user.name="admin"
        user.username = username
        user.set_password(password)
    else:
        click.echo("creating user..")
        user = User(username = username,name="admin")
        user.set_password(password)
        DB.session.add(user)
    db.session.commit()
    click.echo("done..")

# **************** 模板全局变量注册 ******************************
@app.context_processor      #所有模板都可获取的变量
def inject_user():
    user = User.query.first()
    return dict(user=user)

# ******************* 错误响应 **********************************
# 404 错误
@app.errorhandler(404)      # app.errorhandler中注册错误代码
def page_not_found(e):      # 接受异常信息作为参数
    user = User.query.first()
    return render_template("404_extend.html"),404      # 返回状态码作为第二个参数 ，普通响应函数默认是200，所以不用写

# ******************* 模板过滤器 ************************************
#自定义模板过滤器
@app.template_filter("my_filter")    # 过滤器名称注册
def gf(value):
    return value.replace('name','guof')


# ******************　路由与响应函数 *******************************
# 主页
@app.route("/",methods=['GET','POST'])     #路由注册,未指定methods则默认是只接受get方法
def index():
    # request只有在请求触发时才会包含数据,所以你只能在视图函数内部调用它
    if request.method == "POST":            #根据request.method来判断是GET/POST
        if not current_user.is_authenticated: # 如果当前用户未认证
            flash("not login..")
            return redirect(url_for('index')) # 重定向到主页
        title = request.form.get("title")   
        year = request.form.get("year")
        if not all([title,year]):
            #flash() 函数用来在视图函数里向模板传递提示消息，消息存储在session中
            #get_flashed_messages() 函数则用来在模板中获取提示消息
            flash("title and year are required.")     
            return redirect(url_for('index'))
        elif len(year)!=4 or len(title)>60:
            flash("info format is invalid")
            return redirect(url_for('index'))
        
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("item created.")
        return redirect(url_for('index'))
    else:
        user = User.query.first()
        movies = Movie.query.all()
        return render_template("index_extend.html",movies=movies)

# 删除记录
@app.route("/del/<int:id>",methods=['GET','POST'])
@login_required   
def delMovie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash("item deleted!")
    return redirect(url_for('index'))

# 更新记录
@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie.id)) # 重定向回对应的编辑页面
        movie.title = title  
        movie.year = year  
        db.session.commit()  
        flash('Item updated.')
        return redirect(url_for('index'))  
    else:
        return render_template('edit_extend.html', movie=movie)  

# 登录页面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not all([username,password]):
            flash("invalid input")
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)   #使用flask-login提供的login_user函数
            flash('Login success.')
            return redirect(url_for('index')) # 重定向到主页
        else:
            flash('Invalid username or password.') # 如果验证失败， 显示错误消息
            return redirect(url_for('login')) # 重定向回登录页面 
    else:
        return render_template('login_extend.html')         

#  登出页面
@app.route('/logou')
@login_required
def logout():
    logout_user()
    flash("Goodbye.")
    return redirect(url_for('index')) # 重定向到主页


@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form["name"]
        if not name or len(name)>20:
            flash("invalid username")
            return redirect(url_for('settings'))
        
        current_user.name = name
        db.session.commit()
        flash("settings updated")
        return redirect(url_for('index'))
    else:
        return render_template('settings.html')


# *************************  flask程序启动 *********************************
'''
# 1 实例启动  app.run()
# 2 命令行启动  flask run  启用flask发现机制,默认启动程序在app.py或wsgi.py中,可通过环境变量FLASK_APP来更该改启动程序
'''
if __name__ == "__main__":
    app.run()
