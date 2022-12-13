from email import message
import os
import re
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Requires that "less secure app access" be on
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

SPORTS = [
    "Basketball",
    "Soccer",
    "Frisbee",
    "Football",
    "Criket"
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)



@app.route("/register", methods=["POST"])
def register():

    #Validare submission
    name = request.form.get("name")
    email = request.form.get("email")
    sport = request.form.get("sport")
    if not name or not email or sport not in SPORTS:
        return render_template("failure.html", message="Invaild Registration")

    #Send email
    message = Message("You are registered!", recipients=[email])
    mail.send(message)
    # Remember registrant
   # db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)   

    # Confirm registration
    return render_template("success.html")



