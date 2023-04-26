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

        power_prices['datetime'] = pd.to_datetime(
            power_prices['Delivery Date'].astype(str) + " " + power_prices['Delivery Hour'].astype(int).astype(
                str) + ":00:00")

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
                                  settlement_location: str) -> pd.Series:
        result = self.filter(start_time, end_time, settlement_location)
        result['Hourly Project Settlement'] = result['Settlement Point Price'] * result['generation']
        return result['Hourly Project Settlement']

    def average_monthly_values(self, start_time: datetime, end_time: datetime,
                               settlement_location: str) -> pd.DataFrame:
        result = self.filter(start_time, end_time, settlement_location)
        # TODO: This is duplicated unnecessary filtering
        result['settlement'] = self.hourly_project_settlement(start_time, end_time, settlement_location)
        result['month'] = result['datetime'].dt.month
        result['year'] = result['datetime'].dt.year
        result = result[['month', 'year', 'settlement', 'Settlement Point Price', 'generation']]
        return result.groupby(['year', 'month']).mean()


power_prices = pd.read_parquet("../data/power_prices_data.gzip")
modeled_generation = pd.read_csv("../data/windGenTS.csv")

api_data = Q1APIDataset(power_prices, modeled_generation)
concrete_api = Q1APIImplementation(api_data)