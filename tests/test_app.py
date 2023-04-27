import pytest
from flask import url_for

from resurety_homework.app import add_resources, app


# tests to make sure both web api methods give 200 responses

# This is quick and dirty, but is a fixture that produces a test application.
# There's definitely a better way of making sure not to repeat the setup process
@pytest.fixture(scope="function")
def get_test_app():
    if not app.got_first_request:
        add_resources()
    with app.app_context(), app.test_request_context():
        yield app


@pytest.mark.parametrize("start_time, end_time, settlement_location", [
    (1420088400000, 1514782800000, "HB_HOUSTON"),
    (1420088400000, 1420088400000, "HB_HOUSTON"),
    (1420088400000, 1514782800000, "LZ_WEST")
])
def test_200_response_hourly_project_settlement(get_test_app, start_time, end_time, settlement_location):
    response = get_test_app.test_client().get(url_for("hourlyprojectsettlement",
                                                      start_time=start_time,
                                                      end_time=end_time,
                                                      settlement_location=settlement_location))
    assert response.status_code == 200

@pytest.mark.parametrize("start_time, end_time, settlement_location", [
    (1420088400000, 1514782800000, "HB_HOUSTON"),
    (1420088400000, 1420088400000, "HB_HOUSTON"),
    (1420088400000, 1514782800000, "LZ_WEST")
])
def test_200_response_average_monthly_values(get_test_app, start_time, end_time, settlement_location):
    response = get_test_app.test_client().get(url_for("averagemonthlyvalues",
                                                      start_time=start_time,
                                                      end_time=end_time,
                                                      settlement_location=settlement_location))
    assert response.status_code == 200
