# Using Machine Learning to Predict the Weather ([Powered by Dark Sky](https://darksky.net/poweredby/))
This project is based on a three-part article written by Adam McQuistan in [stackabuse.com](http://stackabuse.com/using-machine-learning-to-predict-the-weather-part-1/).

## Update regarding the weather API
My original disclaimer was Weather Underground ([wunderground.com](https://www.wunderground.com/)) was no longer providing free API accounts. At some point (I don't know exactly when), they discontinued their API service altogether. I have since signed up for a [Dark Sky API](https://darksky.net/dev). They don't have a free tier but they do have a trial account which allows 1,000 API calls per day to evaluate the service. Every API request over the free daily limit costs $0.0001. 

## Summary
I won't go into too much detail about the project since you can go to the original article on stackabuse.com; however, here is a little background if you wish to save time. (Although checkout the series, it's worth the read.) 

The project is split into three separate Jupyter Notebooks: one to collect the weather data from the Wunderground.com developer's API (again I'm using Dark Sky's API), inspect it, and clean it; a second to further refine the features and fit the data to a Linear Regression model; and a third to train and evaluate a deep neural net regressor.

## Changes
For the most part I did not deviate from the author's original process. I did seek to automate and streamline the code. For example, I added a progress bar to the data collection function and created  another function to automatically set a target date that is 1000 days prior to the current date. I automated the code to remove features that did not show a strong correlation and implemented a stepwise regression function to automate removing features that had p-values that were too high. (The original author did this manually.)

## Added modules
Automating the code allowed me to adapt the Python code in the Jupyter Notebooks to regular .py files. Jupyter Notebooks are fantastic tools but I believe the final product should be Python scripts that run in the background. Here are the scripts I added and a quick summary:

1. weather.py- a utility file that contains reused methods and variables
2. collect_weather.py- uses the Requests library to download weather data for 1000 days. Also uses ```os.path.isfile()``` and a ```if/elif/else``` statement to determine whether the data from the first 500 days should be collected, data from the second 500 days should be collected, or no data is to be collected. (This no longer necessary since the daily limit is 1,000 calls.)
3. preprocess.py- creates a Pandas DataFrame from the weather records and cleans the data
4. train_test.py- performs some additional preprocessing and fits the data to a Linear Regression model
5. train_test_dnn- uses the same weather data to train, evaluate, and test a deep neural network regressor

## Still To Do
* Update collect_weather.py to make 1,000 API calls at once instead of 500 over two days
* Update the Jupyter Notebooks for the Dark Sky API
* Replace/remove some deprecated methods in the train_test.py and train_test_dnn.py modules
* Add better documentation in the form of markdown cells to the notebooks.
* Apply the model to future forecasts and validate against actual weather data.
