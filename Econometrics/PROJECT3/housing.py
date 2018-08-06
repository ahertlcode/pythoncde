#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 21:42:02 2018

@author: abayomi
"""
import pandas as pd
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot

file = r'CSUSHPISA.csv'

data = pd.read_csv(file)


series = pd.DataFrame(data, columns=['DATE','CSUSHPISA'])
series = series.set_index('DATE')
print(series)

result = adfuller(series['CSUSHPISA'])

print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))

series.plot()

pyplot.show()
    
"""
The unit root testing result of ADF show that the dataset has a clear trend
This suggests that the time series is not stationary and will require 
differencing to make it stationary, at least a difference order of 1.
"""

autocorrelation_plot(series)

pyplot.show()

# fit model
model = ARIMA(series, order=(10,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())
# plot residual errors
residuals = pd.DataFrame(model_fit.resid)
residuals.plot()
pyplot.show()
residuals.plot(kind='kde')
pyplot.show()
print(residuals.describe())
#print(model_fit.forecast())
print("\nForecast for Three Months:\n",25*"=")
print(model_fit.predict(start=373, end=376))