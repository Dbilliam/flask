from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")

def index():
    return render_template("index.html")


@app.route("/welcome", methods=["POST"])
def welcome():
    # Get request.args
    # Post request.form
    name = request.form.get("name", "ram das")
    return render_template("welcome.html", name=name)






