import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


# g是一个特殊对象，可以把多个函数要使用的对象存储其中；这里把数据连接对象存储其中，调用get_db()时就不会每次都去创建连接
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            # current_app也是一个特殊对象，指向处理请求的Flask应用
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # 诉连接返回类似于字典的行
        g.db.row_factory = sqlite3.Row
    return g.db


# 关闭，从g对象中弹出连接对象，然后关闭
def close_db(e=None):
    db = g.db.pop('db', None)
    if db is not None:
        db.close()

