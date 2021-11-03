# 标识flaskr是一个包

import os
from flask import Flask


def create_app(test_config=None):
    # instance_relative_config 声明配置文件是相对于instance folder的相对路径
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="DEV",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    # 默认配置
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    # 创建instance目录，instance目录是flaskr的上级目录，用来存放本地数据，不应该提交到版本控制系统
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "hello world"

    return app
