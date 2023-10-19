import requests
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token
from flask import Blueprint, render_template, session, abort, redirect, request
from google_auth_oauthlib.flow import Flow

from helpers import h_calendar
from logics.requestLogic import RequestLogic
from logics.userLogic import UserLogic
from models.user import User
from models.request import Request

r_logic = RequestLogic()
u_logic = UserLogic()

views = Blueprint(__name__, 'views')
GOOGLE_CLIENT_ID = "167230941061-vb40s8ndfq464anlef200elgk52kgr2a.apps.googleusercontent.com"
client_config = { "web": {
    "client_id": "167230941061-vb40s8ndfq464anlef200elgk52kgr2a.apps.googleusercontent.com",
    "project_id": "sw-test-project-401720",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": [
      "http://127.0.0.1:5000/callback"
    ]}}

flow = Flow.from_client_config(
    client_config=client_config,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5000/callback")


def login_is_required(function):
    def wrapper():
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/login")
def login():
    authorization_uri, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_uri)


@views.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    if u_logic.read(id_info.get("email")) is None:
        u_logic.create(User(email=id_info["email"], name=id_info["name"]))

    user = u_logic.read(id_info["email"])

    session["google_id"] = id_info["sub"]
    session["name"] = user.name
    session["email"] = user.email
    session["group"] = user.group
    session["notify"] = user.notify

    return redirect("/calendar")


@views.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@views.route("/calendar", methods=["GET", "POST"])
@login_is_required
def calendar():
    today = h_calendar.today()
    months = h_calendar.months
    year = int(today[0])
    month = int(today[1])

    if request.method == "POST":
        month = int(request.form["month"])
        year = int(request.form["year"])
        if month == 0:
            month = 12
            year = year - 1
        if month == 13:
            month = 1
            year = year + 1

    days = h_calendar.days(year, month)

    v_requests = r_logic.filter(f"{year}-{month}")

    users = []
    for i in range(31):
        names = []
        for x in r_logic.filter(date=f"{year}-{month}-{i}", state="accepted"):
            name = u_logic.read(x.user_email).name
            names.append(name)
        users.append(names)

    return render_template("calendar.html",
                           group=session["group"],
                           notify=session["notify"],
                           requests=v_requests,
                           days=days,
                           year=year,
                           month=month,
                           months=months,
                           users=users)


@views.route("/v_request", methods=["GET"])
def v_request():
    group = session["group"]
    if group == "viewer":
        return redirect("/calendar")

    return render_template("request.html", group=group)


@views.route("/manage", methods=["GET", "POST"])
def manage():
    v_requests = []
    users = []
    if request.method == "POST":

        if "r_form" in request.form:
            state = request.form["state"]
            date = request.form["date"]
            r_email = request.form["r_email"]
            v_requests = r_logic.filter(state=state, date=date, email=r_email)

        if "u_form" in request.form:
            u_email = request.form["u_email"]
            name = request.form["name"]
            group = request.form["group"]

            users = u_logic.filter(email=u_email, name=name, group=group)

    group = session["group"]
    if group == "viewer" or group == "employee":
        return redirect("/calendar")

    return render_template("manage.html", requests=v_requests, users=users)


@views.route("/create_request", methods=["POST"])
def create_request():
    email = session["email"]
    date = request.form["date"]
    r_logic.create(Request(email, date))
    return redirect("/v_request")


@views.route("/delete_request", methods=["POST"])
def delete_request():
    user_email = request.form["user_email"]
    date = request.form["date"]
    data = r_logic.read(user_email=user_email, date=date)

    r_logic.delete(data)
    return redirect("/manage")


@views.route("/update_request", methods=["POST"])
def update_request():
    user_email = request.form["user_email"]
    date = request.form["date"]
    data = r_logic.read(user_email=user_email, date=date)

    if "state" in request.form:
        state = request.form["state"]
        data.state = state
        r_logic.update(data)
        return redirect("/manage")

    return render_template("request_update.html", request=data)


@views.route("/update_user", methods=["POST"])
def update_user():
    email = request.form["email"]
    data = u_logic.read(email=email)

    if "group" in request.form:
        group = request.form["group"]
        data.group = group
        u_logic.update(data)
        return redirect("/manage")

    if "date" in request.form:
        date = request.form["date"]
        new_request = Request(email, date)
        r_logic.create(new_request)
        return redirect("/manage")

    return render_template("user_update.html", user=data)


@views.route("/update_notify", methods=["POST"])
def update_notify():
    email = session["email"]
    user = u_logic.read(email)
    if user.notify == 1:
        user.notify = 0
    else:
        user.notify = 1

    u_logic.update(user)
    session["notify"] = user.notify
    return redirect("/calendar")
