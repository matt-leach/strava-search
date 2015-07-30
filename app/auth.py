import requests
from stravalib.client import Client
from flask import request, render_template, session, redirect, g
from app import app


@app.before_request
def redirect_not_logged_in():
    if request.endpoint not in ["auth", "home"] and '/static/' not in request.path:
        if "token" not in session:
            return redirect("/")


@app.route("/auth")
def auth():
    try:
        code = request.args["code"]
        c = Client()
        token = c.exchange_code_for_token(app.config['STRAVA_ID'], app.config['STRAVA_SECRET'], code)
    except (KeyError, requests.exceptions.HTTPError):
        return redirect("/")

    session["token"] = c.access_token = token
    a = c.get_athlete()  # Technically shouldn't be needed as the athlete details are returned in the oauth call
    session["athlete"] = {"name": a.firstname, "picture": a.profile_medium, "id": a.id}

    # lookup athlete in db
    cur = g.db.execute('select * from users where id = {}'.format(a.id))
    x = cur.fetchall()
    print x
    if not x:
        # Create the object in the db
        cur = g.db.cursor()
        cur.execute('insert into users (id, name, picture) values (?, ?, ?)', (a.id, a.firstname, a.profile))
        g.db.commit()
    cur.close()

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
