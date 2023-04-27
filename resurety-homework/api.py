import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime


@dataclass(init=False)
class Q1APIDataset:
    data: pd.DataFrame

    def __init__(self, power_prices: pd.DataFrame, generation_data: pd.DataFrame):
        """
        Initializes a Q1APIDataset object. This constructor assumes the input data follows the schema of the sample information provided.

        :param power_prices: a pd.DataFrame containing information about power prices
        :param generation_data: a pd.DataFrame containing the modeled generation over time.
        """
        generation_data['datetime'] = pd.to_datetime(generation_data['time'])
        generation_data = generation_data[['datetime', 'generation']]

        # I was confused about that "delivery interval" field - what's that about?
        # It turns out that instead of using a normal timestamp, datetime records are instead broken into
        # - Date (self explanatory)
        # - Delivery hour (mostly self explanatory, but there's some 24s in here which I just assumed mapped to 12:00am)
        # - Delivery Interval - after doing more research on some Ercot data, these are used to represent 15 minute intervals in an hour

        # Because I discovered this after a decent amount of work was put into the API, this is just a patch fix.
        # Instead of this I could have simply filtered out duplicates of location and datetime, leaving me with only a
        # single interval per hour.
        # But I didn't do that for some reason. This transformation is super slow because I didn't know how to think
        # about it in any way other than as a lambda function, which doesn't take advantage of pandas optimization.
        power_prices['datetime'] = power_prices.apply(lambda entry: f"{entry['Delivery Date']} {str(int(entry['Delivery Hour'])).zfill(2)}:{str(int(15 * (entry['Delivery Interval'] - 1))).zfill(2)}:00",
                                                      axis=1)
        power_prices['datetime'] = pd.to_datetime(power_prices['datetime'], format="%m/%d/%Y %H:%M:%S")

        self.data = generation_data.merge(power_prices, left_on="datetime", right_on="datetime")


@dataclass
class Q1API(ABC):
    dataset: Q1APIDataset

    @abstractmethod
    def hourly_project_settlement(self, start_time: datetime, end_time: datetime, settlement_location: str):
        ...

    @abstractmethod
    def average_monthly_values(self, start_time: datetime, end_time: datetime, settlement_location: str):
        ...


class Q1APIImplementation(Q1API):
    def filter(self, start_time: datetime, end_time: datetime, settlement_location: str) -> pd.DataFrame:
        result = self.dataset.data.loc[(self.dataset.data['Settlement Point Name'] == settlement_location) & (
                self.dataset.data['datetime'] >= start_time) & (self.dataset.data['datetime'] < end_time)]
        return result

    def hourly_project_settlement(self, start_time: datetime, end_time: datetime,
                                  settlement_location: str):
        data = self.filter(start_time, end_time, settlement_location)
        return Q1APIImplementation.__get_hourly_project_settlement_from_filtered_dataframe(data)

    @classmethod
    def __get_hourly_project_settlement_from_filtered_dataframe(cls, data: pd.DataFrame):
        data['Hourly Project Settlement'] = data['Settlement Point Price'] * data['generation']
        data = data[['datetime', 'Hourly Project Settlement']]
        data.reset_index(drop=True, inplace=True)
        return data

    def average_monthly_values(self, start_time: datetime, end_time: datetime,
                               settlement_location: str) -> pd.DataFrame:
        data = self.filter(start_time, end_time, settlement_location)
        return Q1APIImplementation.__get_average_monthly_values_from_filtered_dataframe(data)

    @classmethod
    def __get_average_monthly_values_from_filtered_dataframe(cls, data: pd.DataFrame):
        settlement_df = Q1APIImplementation.__get_hourly_project_settlement_from_filtered_dataframe(data)
        data = data.merge(settlement_df, left_on="datetime", right_on="datetime")
        data['month'] = data['datetime'].dt.month
        data['year'] = data['datetime'].dt.year
        data = data[['month', 'year', 'Hourly Project Settlement', 'Settlement Point Price', 'generation']]
        return data.groupby(['year', 'month']).mean()


power_prices = pd.read_parquet("../data/power_prices_data.gzip")
modeled_generation = pd.read_csv("../data/windGenTS.csv")

api_data = Q1APIDataset(power_prices, modeled_generation)
concrete_api = Q1APIImplementation(api_data)