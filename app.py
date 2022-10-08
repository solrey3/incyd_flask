from flask import Flask, redirect, url_for, render_template, request, session, flash
from views import views
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn

app.register_blueprint(views, url_prefix="")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        # conn = get_db_connection()
        # query_string = f'SELECT * FROM users WHERE name = "{user}"'
        # found_user = conn.execute(query_string)
        
        found_user = User.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
        else:
            usr = User(user, None)
            db.session.add(usr)
            db.session.commit()
        
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session['email'] = email
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit() 
            flash("Email was saved.")
        else:
            if "email" in session:
                email = session ["email"]
    else:
        flash("You are not logged in!")
        return render_template("login.html")

    return render_template("user.html", email=email)

@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)