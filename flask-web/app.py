from forms import LoginForm, RegisterForm
from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from models import db, login, UserModel
from nps_api import webcams


app = Flask(__name__)
app.secret_key = "PC_LOAD_LETTER"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login.init_app(app)


def add_user(email, password):
    # check if email or username exits
    user = UserModel()
    user.set_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email="lhhung@uw.edu").first()
    if user is None:
        add_user("lhhung@uw.edu", "qwerty")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    title = "Home App"
    return render_template("home.html", title=title)


@app.route("/")
def redirectToLogin():
    return redirect("/login")


@app.route("/about")
def about():
    title = "About Us"
    return render_template("about.html", title=title)

@app.route("/webcam")
def webcam():
    title = "Active Park Webcams"
    return render_template("webcam.html", title=title, cams=webcams())


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login Page"
    form = LoginForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(pw):
                login_user(user)
                return redirect("/home")
            elif user is not None and not user.check_password(pw):
                flash(f"Incorrect email or password. Please try again.")
    return render_template("login.html", title=title, form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Registration Page"
    form = RegisterForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email, password)
                flash("Registration Completed!")
                return redirect("/login")
            elif user is not None and user.check_password(password):
                login_user(user)
                return redirect("/home")
            else:
                flash("Email has already been taken. Please try another email.")
    return render_template("register.html", title=title, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def access_denied(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
