import requests
import os

from flask import Flask, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session

CLIENT_ID = ''
CLIENT_SECRET = ''
AUTH_URL = 'https://cloud.ouraring.com/oauth/authorize'
TOKEN_URL = 'https://api.ouraring.com/oauth/token'

app = Flask(__name__)


@app.route('/oura_login')
def oura_login():
    """Redirect to the OAuth provider login page.
    """

    oura_session = OAuth2Session(CLIENT_ID)

    # URL for Oura's authorization page.
    authorization_url, state = oura_session.authorization_url(AUTH_URL)
    session['oauth_state'] = state
    print("LOGING")
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """Retrieve acces_token from Oura response url. Redirect to profile page.
    """

    oura_session = OAuth2Session(CLIENT_ID, state=session['oauth_state'])
    session['oauth'] = oura_session.fetch_token(
                        TOKEN_URL,
                        client_secret=CLIENT_SECRET,
                        authorization_response=request.url)

    return redirect(url_for('.profile'))


@app.route('/profile')
def profile():
    """User profile.
    """
    oauth_token = session['oauth']['access_token']
    result = requests.get('https://api.ouraring.com/v1/userinfo?access_token=' + oauth_token)
    return str(result.json()) 


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='ec2-52-207-227-2.compute-1.amazonaws.com', port="3030")
