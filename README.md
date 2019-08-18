# SimpleLogin Flask Example

An example of a Flask application that implements "Login with SimpleLogin"

To run the app, please set the env variables for your SimpleLogin App

```bash
export CLIENT_ID={your_app_id}
export CLIENT_SECRET={your_app_secret}
```

Then install the dependencies

```bash
pip3 install -r requirements.txt
```

Run the code

```bash
flask run
```

Now if you open http://localhost:5000, you should be able to login with SimpleLogin!

