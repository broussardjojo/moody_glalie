import pandas as pd
import pytest

from resurety_homework.api import concrete_api
from datetime import datetime

# Guaranteeing that the answer is correct and unchanging may not be in the scope of unit tests.
# My unit tests will essentially just assert that all irrelevant entries are filtered out before returning to the user.
@pytest.mark.parametrize("start_time, end_time, settlement_location", [
    (1420088400000, 1514782800000, "HB_HOUSTON"),
    (1420088400000, 1420088400000, "HB_HOUSTON"),
    (1420088400000, 1514782800000, "LZ_WEST")
])
def test_api_hourly_project_settlement(start_time, end_time, settlement_location):
    result = concrete_api.hourly_project_settlement(pd.Timestamp(start_time), pd.Timestamp(end_time), settlement_location)
    assert len(result) == len(result.loc[(result['datetime'] >= pd.Timestamp(start_time)) & (result['datetime'] < pd.Timestamp(end_time))])

@pytest.mark.parametrize("start_time, end_time, settlement_location", [
    (1420088400000, 1514782800000, "HB_HOUSTON"),
    (1420088400000, 1420088400000, "HB_HOUSTON"),
    (1420088400000, 1514782800000, "LZ_WEST")
])
def test_api_average_monthly_values(start_time, end_time, settlement_location):
    result = concrete_api.average_monthly_values(pd.Timestamp(start_time), pd.Timestamp(end_time), settlement_location)
    for stamp in result.index:
        assert pd.Timestamp(start_time) <= stamp < pd.Timestamp(end_time)