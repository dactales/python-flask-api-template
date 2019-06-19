from flask import jsonify, Blueprint, abort, render_template
from flask_security import current_user
from .config import config

webapp = Blueprint("webapp", __name__)


@webapp.route("/")
def index():
    return render_template("index.jade", **locals())


@webapp.route("/profile")
def profile():
    return render_template("profile.jade", **locals())
