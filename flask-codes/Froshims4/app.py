from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
db = SQL("sqlite:///froshim.db")

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee"
]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/deregister", methods=["POST"])
def deregister():
    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?" , id)
    return redirect("/registrants")


@app.route("/register", methods=["POST"])
def register():

    #Validare submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html", message="Invaild Registration")

    # Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)   

    # Confirm registration
    return redirect("/registrants") 

@app.route("/registrants")    
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)



