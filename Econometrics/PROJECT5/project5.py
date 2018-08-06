#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 17:55:53 2018

@author: abayomi

VaR
An investment fund has 100,000 Apple shares.

Solution 1.
Quantify the Maximum Expected Loss for the next day using a Value-at-Risk (VaR) model.

Confidence level: 95%
Volatility: 2.5%
Current stock price: $126
Implement VaR in Python and Excel. 

Solution 2.       
Quantify the Maximum Expected Loss for the next day using a Value-at-Risk (VaR) model.

Confidence level: 95%
Volatility: Forecasted
Forecast the volatility using a GARCH(1,1) programmed in Python.
Stock price: closing price from Google Finance, Yahoo Finance, Quandl, CityFALCON, or another similar source
"""

import fix_yahoo_finance as yf
import pandas as pd
import datetime
import arch
import numpy as np
from scipy.stats import norm


# pylint: disable=C0103
yf.pdr_override()

#Solution 1
stock_units = 100000
stock_price = 126

portfolio_value = stock_units * stock_price

conf_level = 0.95
number_of_days = 1
volatility = 2.5/100
z_score = norm.ppf(conf_level)

VaR_1 = portfolio_value * z_score * volatility
print("First Solution\r\n",16*"=","\r\nHolding = ",portfolio_value, "VaR = ", round(VaR_1,4), "in ",number_of_days, "Days @ z = ",z_score,"\r\n\r\n")

#Solution 2
#Forecasting volatility using GARCH(1, 1)
startdate = datetime.datetime(2017, 6, 30)
enddate = datetime.datetime(2018, 6, 30)
df = pd.DataFrame()
df = yf.download('AAPL', start=startdate, end=enddate)
del df['Open']
del df['High']
del df['Low']
del df['Adj Close']
del df['Volume']

df['log_price'] = np.log(df['Close'])
df['pct_change'] = df['log_price'].diff()

df['stdev21'] = df['pct_change'].rolling(window=21, center=False).std()
df['hvol21'] = df['stdev21'] * (252**0.5) # Annualize.
df['variance'] = df['hvol21']**2
df = df.dropna() # Remove rows with blank cells.

returns = df['pct_change'] * 100
am = arch.arch_model(returns)

res = am.fit(disp='off')
print("\r\n\r\nOutput of the GARCH model Forecasting Volatility of APPLE STOCK AAPL\r\n",70*"=")
print(res.summary())

df['forecast_vol'] = 0.1 * np.sqrt(res.params['omega'] + res.params['alpha[1]'] * res.resid**2 + res.conditional_volatility**2 * res.params['beta[1]'])

print("\r\nDataFrame Tail Display\r\n",25*"=", df.tail())

"""
 From the data downloaded from yahoo finance
 stock_price = 185.110001
 forecasted_volatility = 0.108576
 for the same day.
"""
 
 #Solution 1
stock_units = 100000
stock_price = 185.110001

portfolio_value = stock_units * stock_price

conf_level = 0.95
number_of_days = 1
volatility = 0.108576
z_score = norm.ppf(conf_level)

VaR_1 = portfolio_value * z_score * volatility
print("\r\n\r\nSecond Solution\r\n",16*"=","\r\nHolding = ",portfolio_value, "VaR = ", round(VaR_1,4), "in ",number_of_days, "Days @ z = ",z_score)