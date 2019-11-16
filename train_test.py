import pickle

import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, median_absolute_error
from sklearn.model_selection import train_test_split

with open('end-part1_df.pkl', 'rb') as fp:
    df = pickle.load(fp)

df_corr = df.corr()[['temperatureMean']].sort_values('temperatureMean')
df_corr_fil = df_corr[abs(df_corr['temperatureMean']) > 0.55]

unwanted = ['temperatureMin', 'temperatureMax', 'temperatureMean']
predictors = df_corr_fil.index.tolist()
predictors = [i for i in predictors if i not in unwanted]

df2 = df[['temperatureMean'] + predictors]

X = df2[predictors]
y = df2['temperatureMean']
alpha = 0.05


def stepwise_selection(
    X, y, initial_list=predictors, threshold_out=alpha, verbose=True
):
    """ Perform a forward-backward feature selection
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features
    See https://en.wikipedia.org/wiki/Stepwise_regression for the details
    """
    included = list(initial_list)
    while True:
        changed = False
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max()  # null if pvalues is empty
        if worst_pval > threshold_out:
            changed = True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return included


result = stepwise_selection(X, y)

print('resulting features:')
print(result)

X = X[result]
model = sm.OLS(y, X).fit()
print(model.summary())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=12
)

regressor = LinearRegression()

regressor.fit(X_train, y_train)

prediction = regressor.predict(X_test)

print(f'The Explained Variance: {regressor.score(X_test, y_test):.2f}')
print(
    f'The Mean Absolute Error: {mean_absolute_error(y_test, prediction):.2f} degrees celcius'
)
print(
    f'The Median Absolute Error: {median_absolute_error(y_test, prediction):.2f} degrees celcius'
)
