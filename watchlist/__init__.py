import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from watchlist.settings import DebugMode,TestingMode  # 设置模式

app = Flask(__name__)

#**********************  SQLAlchemy扩展　*****************************
# sqlite,文件型数据库
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"
#定位到项目目录下，不在包目录下
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(os.path.dirname(app.root_path),"data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
 #初始化db对象
db = SQLAlchemy(app)   

# ********************** 开发模式设置 *************************
app.config.from_object(DebugMode)    #开启DEBUG模式，直接在前端页面显示错误代码
#app.config.from_object(TestingMode)  #而在TESTING模式下前端页面之会提示错误，并不会有具体代码

#****************** login manager用户认证扩展 ***************************
#　登录管理(login manager)包含了让你的应用和 Flask-Login 协同工作的代码
login_manager = LoginManager(app)
login_manager.login_view = 'login'                    #默认视图
#实现回调函数user_loader,用于从会话中存储的用户 ID 重新加载用户对象
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User     # 防止循环调用，放在函数内，只用函数调用时才导入
    user = User.query.get(int(user_id))
    return user

# *********************** flask 上下文变量  ******************************
@app.context_processor      #所有模板都可获取的变量
def inject_user():
    from watchlist.models import User    # 防止循环调用 
    user = User.query.first()
    return dict(user=user)

# 防止循环调用，放在尾部
from watchlist import views, errors, comands








