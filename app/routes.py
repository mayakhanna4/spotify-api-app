from app import app
from flask import render_template, flash, redirect,url_for, request, g
from app.forms import *
import json
import requests
import base64
import urllib

#  Client Keys
CLIENT_ID = "0a4ec870c47b42999fb63236b1a6aadb"
CLIENT_SECRET = "1cd80ef407604225a197ca097c173b55"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Maya'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)
    #if form.validate_on_submit():
    #    flash('Login requested for user {}, remember_me={}'.format(
    #        form.username.data, form.remember_me.data))
    #   url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    #    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    #    return redirect(auth_url)
        #return redirect(url_for('index'))
    #return render_template('login.html', title='Sign In', form=form)

@app.route("/callback")
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    return render_template("index.html",sorted_array=display_arr)

@app.route('/search',methods =['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash(form.term.data)
        return redirect(url_for('search'))
    return render_template('search.html', title='Search', form=form)
