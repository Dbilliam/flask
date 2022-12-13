from email import message
from flask import Flask, redirect, render_template, request


app = Flask(__name__)

REGISTRANTS = {}



COURSE = [
    "BCOM",
    "BA",
    'BSC',
    "BCA"
]

SPORTS = [
    "Basketball",
    "Soccer",
    "Football",
    "Running",
    "Criket"
]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS, course=COURSE)

@app.route("/register", methods=["POST"])   
def register():
    # Validate submission
    name = request.form.get("name")
    if not name:

    # if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        return render_template("failure.html" , message="Missing Name") 

    # if not request.form.get("sport") not in SPORTS:
    #     return render_template("failure.html" , message="Missing Name") 
    sport = request.form.get("sport")
    if not sport:
        return render_template("failure.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("failure.html", message="Invaild Sport")    

    # Validate course
    course = request.form.get("course")
    if not course:
        return render_template("failure.html", message="Missing Course")
    if course not in COURSE:
        return render_template("failure.html", message="Invalid Course")
    
    
    #Remember registrant
    REGISTRANTS[name] = sport
    
    #Confirm registration 

    # return render_template("success.html") 
    return redirect("/registrants")

@app.route("/registrants")    
def registrants():
    return render_template("registrants.html", registrants=REGISTRANTS)