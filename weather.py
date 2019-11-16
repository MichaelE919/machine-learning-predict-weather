import os
import time
from collections import namedtuple
from datetime import datetime, timedelta

import requests
from pyprind import ProgBar

loc = '30.578806,-97.853065'

API_KEY = os.environ.get('MY_API_KEY')
BASE_URL = 'https://api.darksky.net/forecast/{}/{},{}'

features = [
    'date',
    'temperatureMean',
    'dewPoint',
    'pressure',
    'humidity',
    'temperatureMax',
    'temperatureMin',
    'precipProbability',
]
DailySummary = namedtuple('DailySummary', features)


def extract_weather_data(url, api_key, target_date, days):
    """Call Wunderground API to extract weather data."""
    records = []
    bar = ProgBar(days)
    for _ in range(days):
        request = BASE_URL.format(
            API_KEY, loc, target_date.strftime('%Y-%m-%dT%H:%M:%S')
        )
        response = requests.get(request)
        if response.status_code == 200:

            def get_mean_temp():
                """Return average temperature across a 24 hour period."""
                total_temp = 0
                for i in range(len(hdata)):
                    try:
                        total_temp += hdata[i]['temperature']
                    except KeyError:
                        total_temp += hdata[i-1]['temperature']
                meanTemp = total_temp / 24
                return meanTemp

            data = response.json()['daily']['data'][0]
            hdata = response.json()['hourly']['data']
            try:
                records.append(
                    DailySummary(
                        date=target_date,
                        temperatureMean=get_mean_temp(),
                        dewPoint=data['dewPoint'],
                        pressure=data['pressure'],
                        humidity=data['humidity'],
                        temperatureMax=data['temperatureMax'],
                        temperatureMin=data['temperatureMin'],
                        precipProbability=data['precipProbability'],
                    )
                )
            except KeyError:
                records.append(
                    DailySummary(
                        date=target_date,
                        temperatureMean=get_mean_temp(),
                        dewPoint=data['dewPoint'],
                        pressure=data['pressure'],
                        humidity=data['humidity'],
                        temperatureMax=data['temperatureMax'],
                        temperatureMin=data['temperatureMin'],
                        precipProbability=0,
                    )
                )
        # time.sleep(6)
        bar.update()
        target_date += timedelta(days=1)
    return records


def get_target_date():
    """Return target date 1000 days prior to current date."""
    current_date = datetime.now()
    target_date = current_date - timedelta(days=1000)
    return target_date


def derive_nth_day_feature(df, feature, N):
    nth_prior_measurements = df[feature].shift(periods=N)
    col_name = f'{feature}_{N}'
    df[col_name] = nth_prior_measurements
