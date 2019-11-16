import pickle

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    explained_variance_score,
    mean_absolute_error,
    median_absolute_error,
)
from sklearn.model_selection import train_test_split

with open('end-part1_df.pkl', 'rb') as fp:
    df = pickle.load(fp)

df.index = df.index.values.astype(float)

# First drop the temperatureMax and temperatureMin from the dataframe
df = df.drop(['temperatureMin', 'temperatureMax'], axis=1)

# X will be a pandas dataframe of all columns except temperatureMean
X = df[[col for col in df.columns if col != 'temperatureMean']]

# y will be a pandas series of the temperatureMean
y = df['temperatureMean']

# split data into training set and a temporary set
X_train, X_tmp, y_train, y_tmp = train_test_split(X, y, test_size=0.2, random_state=23)

# split the remaining 20% of data evenly
X_test, X_val, y_test, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.5, random_state=23
)

X_train.shape, X_test.shape, X_val.shape
print(
    f'Training instances   {X_train.shape[0]}, Training features   {X_train.shape[1]}'
)
print(f'Validation instances {X_val.shape[0]}, Validation features {X_val.shape[1]}')
print(f'Testing instances    {X_test.shape[0]}, Testing features    {X_test.shape[1]}')

feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]

regressor = tf.estimator.DNNRegressor(
    feature_columns=feature_cols,
    hidden_units=[50, 50],
    model_dir='~/Projects/machine-learning-predict-weather/tf_models/tf_wx_model',
)


def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    return tf.estimator.inputs.pandas_input_fn(
        x=X, y=y, num_epochs=num_epochs, shuffle=shuffle, batch_size=batch_size
    )


evaluations = []
STEPS = 400
for i in range(100):
    regressor.train(input_fn=wx_input_fn(X_train, y=y_train), steps=STEPS)
    evaluations.append(
        regressor.evaluate(
            input_fn=wx_input_fn(X_val, y_val, num_epochs=1, shuffle=False)
        )
    )

pred = regressor.predict(input_fn=wx_input_fn(X_test, num_epochs=1, shuffle=False))
predictions = np.array([p['predictions'][0] for p in pred])

print(f'The Explained Variance: {explained_variance_score(y_test, predictions):.2f}')
print(
    f'The Mean Absolute Error: {mean_absolute_error(y_test, predictions):.2f} degrees Celcius'
)
print(
    f'The Median Absolute Error: {median_absolute_error(y_test, predictions):.2f} degrees Celcius'
)
