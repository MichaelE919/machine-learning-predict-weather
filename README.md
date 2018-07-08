# Using Machine Learning to Predict the Weather
This project is based on a three-part article written by Adam McQuistan in [stackabuse.com](http://stackabuse.com/using-machine-learning-to-predict-the-weather-part-1/).

## Summary
I won't go into too much detail about the project since you can go to the original article on stackabuse.com; however, here is a little background if you wish to save time. (Although checkout the series, it's worth the read.) 

The project is split into three separate Jupyter Notebooks: one to collect the weather data from the Wunderground.com developer's API, inspect it, and clean it; a second to further refine the features and fit the data to a Linear Regression model; and a third to train and evaluate a deep neural net regressor.

## Changes
For the most part I did not deviate from the author's original process. I did seek to automate and streamline the code. For example, I added a progress bar to the data collection function and created  another function to automatically set a target date that is 1000 days prior to the current date. I automated the code to remove features that did not show a strong correlation and implemented a stepwise regression function to automate removing features that had p-values that were too high. (The original author did this manually.)

## Added modules
Automating the code allowed me to adapt the Python code in the Jupyter Notebooks to regular .py files. Jupyter Notebooks are fantastic tools but I believe the final product should be Python scripts that run in the background. Here are the scripts I added and a quick summary:

1. weather.py- a utility file that contains reused methods and variables
2. collect_weather.py- uses the Requests library to download weather data for 1000 days. Also uses ```os.path.isfile()``` and a ```if/elif/else``` statement to determine whether the data from the first 500 days should be collected, data from the second 500 days should be collected, or no data is to be collected. (The free API account permits no more than 500 calls per 24 hour-period.)
3. preprocess.py- creates a Pandas DataFrame from the weather records and cleans the data
4. train_test.py- performs some additional preprocessing and fits the data to a Linear Regression model
5. train_test_dnn- uses the same weather data to train, evaluate, and test a deep neural network regressor

## Disclamer regarding the Wunderground API
Weather Underground ([wunderground.com](https://www.wunderground.com/weather/api/)) is no longer providing free API accounts.

## Still To Do
There are still some changes I would like to make. I'd like to add better documentation in the form of  markdown cells to the notebooks and convert all the string formatting to the newer "f strings" where I can. I tried to revise as many as I could but there are still a few remaining the use older formatting styles.

Over the next several months I'll see how these models actually do by comparing the predictions of the models to the actual weather data. Depending on those tests, I'll see about tuning the existing models or trying others.
