from watchlist import app, db
from flask import url_for,render_template,request,flash,redirect # 引入Flask类 ,url_for反向解析 
from werkzeug.security import generate_password_hash,check_password_hash  #密码加密、验证
from flask_login import login_user,login_required, logout_user,current_user  #用户认证
from watchlist.models import User, Movie

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

