from flask import jsonify, Blueprint, abort
from flasgger import SwaggerView
from marshmallow import Schema, fields

from . import model


v1 = Blueprint("v1", __name__)


class DemoView(SwaggerView):
    tags = ["demo-tag"]
    summary = "Show the demo"
    description = "Demo description"
    parameters = [
        {
            "name": "echo_string",
            "description": "Echo string",
            "in": "path",
            "type": "string",
            "required": True,
        }
    ]
    responses = {
        200: {"desciption": "Returns Demo Details", "schema": model.DemoSchema}
    }

    def get(self, echo_string="default"):
        """ Get demo details
        """
        result = model.DemoSchema().dump(dict(echo_string=echo_string))
        return jsonify(result.data)


# URL Rules ############################################
v1.add_url_rule(
    "/demo/<echo_string>", view_func=DemoView.as_view("demo"), methods=["GET"]
)
