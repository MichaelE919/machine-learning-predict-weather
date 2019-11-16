import os.path
import pickle
from datetime import timedelta

from weather import API_KEY, BASE_URL, extract_weather_data, get_target_date

filename1 = 'records_pt1.pkl'
filename2 = 'records_pt2.pkl'

if os.path.isfile(filename2):
    print('1000 records already collected from Dark Sky API')

elif os.path.isfile(filename1):
    with open(filename1, 'rb') as fp:
        records = pickle.load(fp)

    target_date = records[-1][0] + timedelta(days=1)

    records += extract_weather_data(BASE_URL, API_KEY, target_date, 500)

    records_length = len(records)
    print(f'{records_length} records collected from Dark Sky API')

    with open(filename2, 'wb') as f:
        pickle.dump(records, f)

    print(f'Weather records from day 2 saved to {filename2}.')

else:
    target_date = get_target_date()

    records = extract_weather_data(BASE_URL, API_KEY, target_date, 500)

    records_length = len(records)
    print(f'{records_length} records collected from Dark Sky API')

    with open(filename1, 'wb') as f:
        pickle.dump(records, f)

    print(f'Weather records from day 1 saved to {filename1}.')
