import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


# 定义一个命令
@click.command('init_db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("init a database")


def init_app(app):
    #  Flask 在返回响应后进行清理的时候调用此函数。
    app.teardown_appcontext(close_db)
    #  添加一个新的 可以与 flask 一起工作的命令。
    app.cli.add_command(init_db_command)


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
    db = g.pop('db', None)
    if db is not None:
        db.close()
