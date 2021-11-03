from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 默认只能接收get请求，也可以通过route装饰器设置请求类型
@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return "get method"
    else:
        return 'post method!'


@app.route('/test')
def test():
    return 'this is test'


# 使用 <value> 可以传递参数,默认是string类型
@app.route('/test/<username>')
def hello_name(username):
    return 'hello %s' % escape(username)


# 使用 <value> 可以传递参数,默认是string类型,其它类型可做限定，
# int、float、path、uuid
# 注意类型和参数之间不能有空格
"""
类型介绍：
string : 接收不带/的字符串
int :接收正整数
float：接收正浮点数
path: 接收可能含有/的字符串
uuid:接收UUID字符串
"""


@app.route('/test/<int:id>')
def get_id(id):
    return 'id is %s' % id


if __name__ == '__main__':
    app.run()

with app.test_request_context():
    print(url_for('index'))
    print(url_for("test"))
    print(url_for("test/liming"))
    print(url_for("test/100"))
