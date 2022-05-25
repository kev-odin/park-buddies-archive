from forms import LoginForm, RegisterForm
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel
from nps_api import webcams, parks


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


@app.route("/")
def index():
    title = "Park Buddies"
    technology_dict = {
        "Python": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/110px-Python-logo-notext.svg.png",
        "Docker": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Docker_logo.svg/512px-Docker_logo.svg.png",
        "Flask": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flask_logo.svg/460px-Flask_logo.svg.png",
        "Nginx": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Nginx_logo.svg/320px-Nginx_logo.svg.png",
        "Bootstrap": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Bootstrap_logo.svg/301px-Bootstrap_logo.svg.png",
        "Gunicorn": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Gunicorn_logo_2010.svg/320px-Gunicorn_logo_2010.svg.png",
        "Amazon Web Services": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/320px-Amazon_Web_Services_Logo.svg.png",
        "National Park Service": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Logo_of_the_United_States_National_Park_Service.svg/184px-Logo_of_the_United_States_National_Park_Service.svg.png",
    }
    return render_template("index.html", title=title, tech=technology_dict)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    title = "Home App"
    services = {
        "Activities": {
            "image": "yakko_50states_384x384.jpg",
            "btn": "Find your activities",
            "endpoint": "activities",
        },
        "Parks by State": {
            "image": "goofy_camping_500x500.jpg",
            "btn": "Find your parks",
            "endpoint": "parkbystate",
        },
        "Webcams": {
            "image": "monkey_selfie_555x555.jpg",
            "btn": "Observe your parks",
            "endpoint": "webcam",
        },
    }
    return render_template("home.html", title=title, services=services)


@app.route("/about")
def about():
    title = "About Us"
    return render_template("about.html", title=title)


@app.route("/activities")
@login_required
def activities():
    title = "Park Activities"
    return render_template("activities.html", title=title)


@app.route("/webcam")
@login_required
def webcam():
    title = "Active Park Webcams"
    return render_template("webcam.html", title=title, cams=webcams())


@app.route("/parkbystate")
@login_required
def parkbystate():
    title = "Park by State"
    return render_template(
        "parkbystate.html", title=title, myData=parks("WA")
    )  # add WA for Saturday demo only


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

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email, password)
                flash("Registration Completed!")
                return redirect(url_for("login"))
            elif user is not None and user.check_password(password):
                login_user(user)
                return redirect(url_for("home"))
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
