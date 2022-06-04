from forms import LoginForm, RegisterForm, SettingsForm, searchForm, ActivitiesForm
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel
from nps_api import webcams, parks, activities as list_activities, activities_parks


app = Flask(__name__)
app.secret_key = "PC_LOAD_LETTER"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login.init_app(app)


def add_user(email, password, state):
    user = UserModel()
    user.set_password(password)
    user.email = email
    user.state = state
    db.session.add(user)
    db.session.commit()


@app.before_first_request
def create_table():
    db.drop_all()
    db.create_all()
    user = UserModel.query.filter_by(email="lhhung@uw.edu").first()
    if user is None:
        add_user("lhhung@uw.edu", "qwerty", "WA")


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
        "Stack Overflow": "https://upload.wikimedia.org/wikipedia/commons/0/02/Stack_Overflow_logo.svg"
    }
    return render_template("index.html", title=title, tech=technology_dict)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    title = "Home App"
    services = {
        "Activities": {
            "image": "goofy_camping_500x500.jpg",
            "btn": "Find your activities",
            "endpoint": "activities",
        },
        "Parks by State": {
            "image": "yakko_50states_384x384.jpg",
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
    profiles = {
        "Kevin Chung": {
            "gif": "https://media.giphy.com/media/l1J9DoKrzHMW8fP3O/giphy.gif",
            "endpoint": "webcam",
            "feat": [
                "User login, registration, and setting",
                "National Park API and webcams",
                "Docker and Bootstrap",
            ],
        },
        "Xingguo Huang": {
            "gif": "https://media.giphy.com/media/1wh06XT53tPGw/giphy.gif",
            "endpoint": "parkbystate",
            "feat": ["Parks by state", "Map widget", "Image carousel"],
        },
        "JP Montagnet": {
            "gif": "https://media.giphy.com/media/DfbpTbQ9TvSX6/giphy.gif",
            "endpoint": "activities",
            "feat": [
                "Park activites",
                "Multi-select query",
                "Official in house Software dev",
            ],
        },
    }
    site = [
        "Search all US National Parks by State.",
        "Determine which activities are available.",
        "Enjoy a live webcam feed directly with our service.",
        "Make edits to your user profile.",
    ]
    return render_template("about.html", title=title, profile=profiles, site=site)


def _activs_parks_xform(data):
    """
    Response data structure is... inconvenient:
    [ { id: <Activity1_id>, name: <Activity1_name>, parks:
        [ { parkCode: <Park1_code>, fullName: <Park1_name>, ... },
          { parkCode: <Park2_code>, fullName: <Park2_name>, ... },
          ... ] },
      { id: <Activity2_id>, name: <Activity2_name>, parks:
        [ { parkCode: <ParkX_code>, fullName: <ParkX_name>, ... },
        [ { parkCode: <ParkY_code>, fullName: <ParkY_name>, ... },
          ... ] },
      ... ]
    Parks info is repeated under every actiity applicable to it.

    Restructure to something more convenient:
    [ { "id": <Park1_code>,
        "name": <Park1_name>,
        "acts": { <Activity1_name>: <bool>,
                  <Activity2_name>: <bool>,
                  ... }},
      { "id": <Park2_code>,
        "name": <Park2_name>,
        "acts": { <Activity1_name>: <bool>,
                  ... }},
      ... ]

    A more compact representation is certainly possible,
    but the above strikes a reasonable balance.
    """
    if data is None:
        return None

    r = {}
    a_names = [x["name"] for x in data]
    for activ in data:
        a_name = activ["name"]
        for park in activ["parks"]:
            p_id = park["parkCode"]
            if p_id not in r:
                r[p_id] = {"name": park["fullName"], "acts": {}}
            r[p_id]["acts"][a_name] = True
    for a_name in a_names:
        for p_id in r.keys():
            if a_name not in r[p_id]["acts"]:
                r[p_id]["acts"][a_name] = False

    results = [{'id': k, 'name': v['name'], 'acts': v["acts"]} for k, v in r.items()]
    print (f"results = {r}")
    return results


@app.route("/activities", methods=["GET", "POST"])
@login_required
def activities():
    title = "Park by Activities"
    form = ActivitiesForm()

    # Available choices, structured as required for SelectField
    # Canned example, a subset of the full set offered by API:
    # choices = [
    #  ('A59947B7-3376-49B4-AD02-C0423E08C5F7', 'Camping'),
    #  ('AE42B46C-E4B7-4889-A122-08FE180371AE', 'Fishing'),
    #  ('BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA', 'Hiking'),
    #  ('F9B1D433-6B86-4804-AED7-B50A519A3B7C', 'Skiing')]
    choices = list_activities()
    form.activs.choices = choices

    # Subset of choices, as needed to both query the API (by id)
    # and to generate results table (by name).
    # Note structure here is dict, rather than list of tuples.
    # Canned example:
    # chosen = {
    #     'A59947B7-3376-49B4-AD02-C0423E08C5F7': 'Camping',
    #     'AE42B46C-E4B7-4889-A122-08FE180371AE': 'Fishing'}
    chosen = {}

    # Results from query of API, restructured for convenience.
    # Canned example:
    # results = {
    #   'jlst': { 'Name': 'Jellystone', 'Camping': True,  'Fishing': False },
    #   'atls': { 'Name': 'Atlantis',   'Camping': False, 'Fishing': True  }}
    results = {}

    if request.method == "GET":
        chosen_ids = chosen.keys()
        form.activs.data = chosen_ids
    elif form.validate_on_submit():
        chosen_ids = request.form.getlist("activs")
        chosen = dict([x for x in choices if x[0] in chosen_ids])
        data = activities_parks(ids=chosen_ids)
        results = _activs_parks_xform(data)
        # results = sorted(results, key=_match_count)
    return render_template("activities.html", title=title,
                           form=form, chosen=chosen, results=results)


@app.route("/webcam")
@login_required
def webcam():
    title = "Active Park Webcams"
    return render_template("webcam.html", title=title, cams=webcams())


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    title = "User Settings"
    form = SettingsForm()

    if request.method == "GET":
        form.email.data = current_user.email
        form.state.data = current_user.state

    if request.method == "POST":
        if form.validate_on_submit():
            user = UserModel.query.filter_by(id=current_user.id).first()
            pw = request.form["password"]

            if user.check_password(pw):
                if request.form["state"] != user.state:
                    flash("State changed successfully.", category="success")
                    user.state = request.form["state"]
                if request.form["email"] != user.email:
                    flash("Email changed successfully.", category="success")
                    user.email = request.form["email"]
                if request.form["new_password"]:
                    flash("Password changed successfully.", category="success")
                    password_change = request.form["new_password"]
                    user.set_password(password_change)

                db.session.commit()
                return render_template(
                    "settings.html", title=title, user=current_user, form=form
                )
            else:
                flash(
                    f"Settings not applied. Incorrect credentials for {current_user.email}",
                    category="warning",
                )
    return render_template("settings.html", title=title, user=current_user, form=form)


@app.route("/parkbystate", methods=["GET", "POST"])
@login_required
def parkbystate():
    title = "Park by State"
    form = searchForm()

    if request.method == "GET":
        form.state.data = current_user.state

    if form.validate_on_submit():
        if request.method == "POST":
            state = request.form["state"]
            return render_template(
                "parkbystate.html",
                title=title,
                myData=parks(state_code=state),
                form=form,
            )

    return render_template(
        "parkbystate.html",
        title=title,
        myData=parks(state_code=current_user.state),
        form=form,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login Page"
    form = LoginForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                flash(
                    f"No account found. Please register for an account with our service.",
                    category="warning",
                )
            elif user and not user.check_password(pw):
                flash(
                    f"Incorrect password. Please try again.",
                    category="warning",
                )
            elif user and user.check_password(pw):
                login_user(user)
                flash(f"Welcome to Park Buddies!", category="success")
                return redirect(url_for("home"))
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
            state = request.form["state"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email, password, state)
                flash("Registration successful.", category="success")
                return redirect(url_for("login"))
            elif user and user.check_password(password):
                login_user(user)
                flash("Registered account found.", category="success")
                return redirect(url_for("home"))
            else:
                flash(
                    "Email has already been taken. Please try another email.",
                    category="warning",
                )
    return render_template("register.html", title=title, form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logout successful.", category="success")
    return redirect(url_for("login"))


@app.errorhandler(401)
def forbidden(e):
    title = "Unauthorized Access"
    return render_template("401.html", title=title), 401


@app.errorhandler(403)
def access_denied(e):
    title = "Forbidden Access"
    return render_template("403.html", title=title), 403


@app.errorhandler(404)
def page_not_found(e):
    title = "Page Not Found"
    return render_template("404.html", title=title), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
