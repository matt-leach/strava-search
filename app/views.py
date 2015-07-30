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
