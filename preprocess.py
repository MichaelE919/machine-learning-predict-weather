import pickle

import pandas as pd

from weather import derive_nth_day_feature, features

with open('records_pt2.pkl', 'rb') as fp:
    records = pickle.load(fp)

df = pd.DataFrame(records, columns=features).set_index('date')

for feature in features:
    if feature != 'date':
        for N in range(1, 4):
            derive_nth_day_feature(df, feature, N)

# make list of original features without temperatureMean, temperatureMin, and temperatureMax
to_remove = [
    feature
    for feature in features
    if feature not in ['temperatureMean', 'temperatureMin', 'temperatureMax']
]

# make a list of columns to keep
to_keep = [col for col in df.columns if col not in to_remove]

# select only the columns in to_keep and assign to df
df = df[to_keep]

df = df.apply(pd.to_numeric, errors='coerce')

# Call describe on df and transpose it due to the large number of columns
spread = df.describe().T

# precalculate interquartile range for ease of use in next calculation
IQR = spread['75%'] - spread['25%']

# create an outliers column which is either 3 IQRs below the first quartile or
# 3 IQRs above the third quartile
spread['outliers'] = (spread['min'] < (spread['25%'] - (3 * IQR))) | (
    spread['max'] > (spread['75%'] + 3 * IQR)
)

# iterate over the precip columns
for precip_col in ['precipProbability_1', 'precipProbability_2', 'precipProbability_3']:
    # create a boolean array of values representing nans
    missing_vals = pd.isnull(df[precip_col])
    df[precip_col][missing_vals] = 0

df = df.dropna()

with open('end-part1_df.pkl', 'wb') as f:
    pickle.dump(df, f)
