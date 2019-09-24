from watchlist import app
from flask import render_template

# ******************* 错误响应 **********************************
# 404 错误
@app.errorhandler(404)      # app.errorhandler中注册错误代码
def page_not_found(e):      # 接受异常信息作为参数
    return render_template("404_extend.html"),404      # 返回状态码作为第二个参数 ，普通响应函数默认是200，所以不用写
