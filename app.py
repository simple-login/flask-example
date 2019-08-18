import requests_oauthlib, os, flask

# Get SimpleLogin AppID, AppSecret from env vars
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

app = flask.Flask("my-app")
app.secret_key = "my-super-secret"  # for flask.session

# This allows us to test the app using HTTP.
# Please make sure to disable it in production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@app.route("/")
def index():
    return """
    <a href="/login">Login with SimpleLogin</a>
    """


@app.route("/login")
def login():
    sl = requests_oauthlib.OAuth2Session(
        CLIENT_ID,
        # this supposes you are running your app on the default port 5000
        redirect_uri="http://localhost:5000/callback",
    )

    redirect_url, state = sl.authorization_url(
        "https://app.simplelogin.io/oauth2/authorize"
    )

    # State is used to prevent CSRF, keep this for later.
    flask.session["oauth_state"] = state

    return flask.redirect(redirect_url)


@app.route("/callback")
def callback():
    sl = requests_oauthlib.OAuth2Session(
        CLIENT_ID, state=flask.session.get("oauth_state")
    )
    # Get the "access token"
    sl.fetch_token(
        "https://app.simplelogin.io/oauth2/token",
        client_secret=CLIENT_SECRET,
        authorization_response=flask.request.url,
    )

    user_info = sl.get("https://app.simplelogin.io/oauth2/userinfo").json()

    # This is where you log user in, for ex via flask-login extension: login_user(user)
    return f"""
    Welcome {user_info["name"]} <br>
    <a href="/">Logout</a> <br>
    Your email is {user_info["email"]} <br>
    And your avatar: <img src="{user_info['avatar_url']}">
    """
