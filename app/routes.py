from app import app
from flask import render_template, flash, redirect,url_for, request, g
#from flask_oauthlib.client import OAuth, OAuthException
from app.forms import *
import json
import requests
import base64
import urllib
import spotipy
import sys

#  Client Keys
CLIENT_ID = "0a4ec870c47b42999fb63236b1a6aadb"
CLIENT_SECRET = "1cd80ef407604225a197ca097c173b55"

username = ""


spotify = spotipy.Spotify()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': username}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    return redirect(auth_url)


@app.route('/search',methods =['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        name = form.term.data
        results = spotify.search(q='artist:' + name, type='artist')
        flash(results)
        return redirect(url_for('search'))
    return render_template('search.html', title='Search', form=form)
