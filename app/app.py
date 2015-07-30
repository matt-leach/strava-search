import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

from secret import SECRET_KEY

# configuration
DATABASE = '/tmp/strava_search.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_users():
    cur = g.db.execute('select name from users order by id desc')
    users = [dict(name=row[0]) for row in cur.fetchall()]
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run()
