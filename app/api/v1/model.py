from datetime import datetime

from marshmallow import Schema, fields, pre_dump


class DemoSchema(Schema):
    demo_string = fields.String(description="A Demo string")
    echo_string = fields.String(description="The Ech string")
    date = fields.Date(description="Date")

    @pre_dump
    def prepare_data(self, data, **kwargs):
        data["date"] = datetime.utcnow()
        data["demo_string"] = "Demo String"
        return data
