from flask import jsonify, Blueprint, abort

webapp = Blueprint("webapp", __name__)


@webapp.route("/")
def index():
    abort(404)
    return jsonify(dict())
