#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 23:01:35 2018

@author: abayomi

2. Calculate the equilibrium foreign exchange using cointegration 
 (use one macroeconomic factor in the analysis).

3. Calculate the equilibrium foreign exchange using cointegration 
 (use two or more macroeconomic factors in the analysis).

There is a need to test whether the spot rates and forward rates are stationary 
before estimating the long run equilibrium relation. There are some common 
methods for testing whether a series is stationary  or  not.  In  this  paper,  
the  Augmented  Dickey-Fuller
"""
import pandas as pd
#from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import adfuller
#from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot

file = r'USD_NGN Historical Data.csv'

data = pd.read_csv(file)


series = pd.DataFrame(data, columns=['Date','Price'])
series = series.set_index('Date')
print(series)

result = adfuller(series['Price'])

print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))

series.plot()

pyplot.show()

"""
From the unit root testing result of ADF it could be seen that there is no clear 
trend in the time series for USD/NGN currency pair in the foreign exchange market.
This suggests that the time series is stationary.
"""
