import os
import time
from collections import namedtuple
from datetime import datetime, timedelta

import requests
from pyprind import ProgBar

API_KEY = os.environ.get('MY_API_KEY')
BASE_URL = 'http://api.wunderground.com/api/{}/history_{}/q/TX/Round_Rock.json'

features = [
    "date", "meantempm", "meandewptm", "meanpressurem", "maxhumidity",
    "minhumidity", "maxtempm", "mintempm", "maxdewptm", "mindewptm",
    "maxpressurem", "minpressurem", "precipm"
]
DailySummary = namedtuple('DailySummary', features)


def extract_weather_data(url, api_key, target_date, days):
    """Call Wunderground API to extract weather data."""
    records = []
    bar = ProgBar(days)
    for _ in range(days):
        request = BASE_URL.format(API_KEY, target_date.strftime('%Y%m%d'))
        response = requests.get(request)
        if response.status_code == 200:
            data = response.json()['history']['dailysummary'][0]
            records.append(
                DailySummary(
                    date=target_date,
                    meantempm=data['meantempm'],
                    meandewptm=data['meandewptm'],
                    meanpressurem=data['meanpressurem'],
                    maxhumidity=data['maxhumidity'],
                    minhumidity=data['minhumidity'],
                    maxtempm=data['maxtempm'],
                    mintempm=data['mintempm'],
                    maxdewptm=data['maxdewptm'],
                    mindewptm=data['mindewptm'],
                    maxpressurem=data['maxpressurem'],
                    minpressurem=data['minpressurem'],
                    precipm=data['precipm']))
        time.sleep(6)
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
