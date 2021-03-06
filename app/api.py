from stravalib import Client
from flask import Flask, request, session, g, render_template, jsonify
from app import app
import json
import time


@app.route('/api/activities', methods=['GET'])
def html_activities():
    user_id = session['athlete']['id']
    # Get max and min distance parameters
    max_dist = int(request.args.get('max', 1000))
    min_dist = int(request.args.get('min', 0))

    q = '%{}%'.format(request.args.get('q', ''))
    cur = g.db.cursor()
    cur.execute('select * from activities \
                where (users_id = ?) and (distance <= ?) and (distance >= ?) \
                and (name like ?) order by start_time desc',
                [user_id, max_dist, min_dist, q])
    activities = cur.fetchall()
    times = [[a[3], 0] for a in activities]
    activities = [{'name': a[1], "distance": a[2], "id": a[0]} for a in activities]
    return render_template('activities.html', activities=activities, times=times)
