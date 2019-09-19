from flask import Flask
app = Flask(__name__)

# flask route
@app.route("/")
def hello():
    return "welcome to my watchlist!"

