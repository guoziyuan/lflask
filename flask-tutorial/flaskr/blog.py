from flask import (
    flash, Blueprint, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not title:
            error = 'title is required'
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template("blog/create.html")


# 获取一个blog对象
def get_post(id, check_author=True):
    # sql换行，末尾空格不能少
    post = get_db().execute(
        "SELECT p.id, title, body, author_id, created, username "
        "FROM post p JOIN user u ON p.author_id = u.id "
        "WHERE p.id = ?", (id,)
    ).fetchone()
    if post is None:
        abort(404, "post id {0} is not exist".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


# 更新
@bp.route("/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title is None:
            flash("title is required")
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ? , body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/update.html", post=post)


# 删除
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
