from watchlist import app,db
from faker import Factory   # 使用faker生成测试数据
from watchlist.models import User, Movie
import click   #命令行工具

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