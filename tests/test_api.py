import pytest

from resurety_homework.api import concrete_api

@pytest.mark.parametrize("start_time, end_time, settlement_location", [
    (1420088400000, 1514782800000, "HB_HOUSTON"),
    (1420088400000, 1420088400000, "HB_HOUSTON"),
    (1420088400000, 1514782800000, "LZ_WEST")
])
def test_api_hourly_project_settlement(start_time, end_time, settlement_location):
    ...