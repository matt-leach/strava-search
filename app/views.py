from stravalib import Client

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from app import app


@app.route('/')
def home():
    url = Client().authorization_url(client_id=app.config['STRAVA_ID'],
                                     redirect_uri="http://localhost:5000/auth",
                                     approval_prompt="force")
    return render_template('home.html', auth_url=url)


@app.route('/activities')
def activities():
    user_id = session['athlete']['id']
    cur = g.db.cursor()
    cur.execute('select * from activities where users_id = ?', [user_id])
    activities = cur.fetchall()
    activities = [{'name': a[1], "distance": a[2]} for a in activities]
    activities.reverse()
    return render_template('search_activities.html', activities=activities)


@app.route('/activities/load')
def load_activities():
    users_id = session['athlete']['id']
    c = Client(access_token=session['token'])
    activities = list(c.get_activities())
    cur = g.db.cursor()

    # Delete activities before loading to prevent id clashes
    cur.execute('delete from activities where users_id = ?', [users_id])
    g.db.commit()

    # TODO: bulk create
    for a in activities:
        cur.execute('insert into activities (id, name, distance, start_time, users_id) values (?, ?, ?, ?, ?)',
                    (a.id, a.name, int(a.distance) / 1609, a.start_date, users_id))
        g.db.commit()
    cur.close()

    return redirect('/activities')
