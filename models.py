'''
模型类继承自db.Model
字段创建使用db.Column()方式
flask类主键需要显示指定，django中如果没有显式指定主键，是默认生成

常用字段类型
db.Integer
db.String(size)
db.Text
db.Datetime
db.Float
db.Boolean
'''
'''
class User(db.Model):  
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Moive(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))
'''