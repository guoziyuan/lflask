import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 注册
@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'username can not be None'
        elif not password:
            error = 'please input password'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'user {} is already registered'.format(username)
        if error is None:
            db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')


# 登录
@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        # 根据用户名查询用户
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        error = None
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        # 校验通过
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # 重定向到首页
            return redirect(url_for("index"))
        # 提示错误
        flash(error)
    return render_template('auth/login.html')


# 获取用户信息  在视图函数之前运行的函数，不论其 URL 是什么
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


# 登出
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


# 定义一个装饰器，如果已登录，返回原视图，如果没有登录，放回登录视图
def login_required(view):
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None:
            return register(url_for('auth.login'))
        return view(kwargs)

    return wrapper_view


