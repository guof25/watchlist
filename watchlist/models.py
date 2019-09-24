'''
db.Model 模型类基类
字段创建：使用db.Column()方式
主键创建： flask类主键需要显示指定，django中如果没有显式指定主键，是默认生成
常用字段类型：
db.Integer
db.String(size)
db.Text
db.Datetime
db.Float
db.Boolean
'''

'''
#  UserMixin类提供了 is_authenticated,is_active,is_anonymous,get_id()属性/方法的默认实现，继承它即可使用
'''

from watchlist import db
from flask_login import UserMixin  #用户认证
from werkzeug.security import generate_password_hash,check_password_hash  #密码加密、验证

class User(db.Model,UserMixin):                  
    __tablename__ = "wl_user"                     # 数据库表名，未定义则默认是类名
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

