from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from config import Config
from models import db, User, ServiceCall
from forms import LoginForm, ServiceCallForm, RegistrationForm
import datetime
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    service_calls = ServiceCall.query.all()
    return render_template("service_call_list.html", service_calls=service_calls)


@app.route("/open_service_call", methods=["GET", "POST"])
@login_required
def open_service_call():
    form = ServiceCallForm()
    if form.validate_on_submit():
        call_id = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=7))
        service_call = ServiceCall(
            department=form.department.data,
            requesting_user=current_user.username,
            urgency=form.urgency.data,
            call_type=form.call_type.data,
            description=form.description.data,
        )
        db.session.add(service_call)
        db.session.commit()
        flash("Service call created successfully")
        return redirect(url_for("index"))
    return render_template("open_service_call.html", form=form)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if current_user.privilege < 2:
        flash("Access denied")
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            name=form.name.data,
            role=form.role.data,
            department=form.department.data,
            privilege=form.privilege.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully")
        return redirect(url_for("admin"))
    return render_template("admin.html", form=form)


@app.route("/complete_call/<int:call_id>")
@login_required
def complete_call(call_id):
    service_call = ServiceCall.query.get_or_404(call_id)
    service_call.completion_deletion_date = datetime.datetime.utcnow()
    service_call.completing_deleting_user = current_user.username
    db.session.commit()
    flash("Service call completed successfully")
    return redirect(url_for("index"))


@app.route("/delete_call/<int:call_id>")
@login_required
def delete_call(call_id):
    service_call = ServiceCall.query.get_or_404(call_id)
    if (
        current_user.privilege < 2
        and service_call.requesting_user != current_user.username
    ):
        flash("Access denied")
        return redirect(url_for("index"))
    service_call.completion_deletion_date = datetime.datetime.utcnow()
    service_call.completing_deleting_user = current_user.username
    db.session.commit()
    flash("Service call deleted successfully")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
