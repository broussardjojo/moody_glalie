import datetime

from flask import Flask
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
from moody_glalie.api import concrete_api

app = Flask(__name__)
api = Api(app)

class HourlyProjectSettlement(Resource):
    get_args = {
        'start_time': fields.DateTime(
            format="timestamp_ms",
            required=True
        ),
        'end_time': fields.DateTime(
            format="timestamp_ms",
            required=True
        ),
        'settlement_location': fields.Str(
            required=True
        )
    }

    @use_args(get_args, as_kwargs=True, location="query")
    def get(self, start_time: datetime.datetime, end_time: datetime.datetime, settlement_location: str):
        answer = concrete_api.hourly_project_settlement(start_time, end_time, settlement_location)
        return answer.to_json()

class AverageMonthlyValues(Resource):
    get_args = {
        'start_time': fields.DateTime(
            format="timestamp_ms",
            required=True
        ),
        'end_time': fields.DateTime(
            format="timestamp_ms",
            required=True
        ),
        'settlement_location': fields.Str(
            required=True
        )
    }

    @use_args(get_args, as_kwargs=True, location="query")
    def get(self, start_time: datetime.datetime, end_time: datetime.datetime, settlement_location: str):
        answer = concrete_api.average_monthly_values(start_time, end_time, settlement_location)
        return answer.to_json()


def add_resources():
    api.add_resource(HourlyProjectSettlement, "/hourly_project_settlement")
    api.add_resource(AverageMonthlyValues, "/average_monthly_values")

if __name__ == "__main__":
    add_resources()
    app.run(port=5001, debug=True)