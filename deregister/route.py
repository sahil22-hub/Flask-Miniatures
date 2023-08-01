
from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

dbName = "data.db"


SPORTS = [
    "Basketball",
    "Soccer",
    "Cricket",
    "Table Tennis"
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    print('id')
    print(id)
    if id:
        conn = sqlite3.connect(dbName)

    # Create a cursor object to interact with the database
        db = conn.cursor()
        db.execute("DELETE FROM register WHERE id = ?", id)
        conn.commit()
    return redirect("/registrants")


@app.route("/register", methods=["POST"])
def register():

    # Validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    conn = sqlite3.connect(dbName)
    print('database connection1')

    # Create a cursor object to interact with the database
    db = conn.cursor()
    print('database connection2')
    # Remember registrant
    db.execute("INSERT INTO register(name, sport) VALUES(?, ?)",
               (name, sport))
    conn.commit()
    print('database connection3')

    # Confirm registration
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    conn = sqlite3.connect(dbName)
    db = conn.cursor()
    registrants = db.execute("SELECT * FROM register")
    all_rows = registrants.fetchall()
    conn.commit()
    print('data display:')
    print(all_rows)
    return render_template("registrants.html", registrants=all_rows)
