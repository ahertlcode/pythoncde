#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  16 12:01:35 2018

@author: abayomi
WQU 613 Econometrics – 0418 - A
Final Project
Forecasting Gold Price
"""
from scipy import stats
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


"""
gold(t) = alpha + beta + gold(t-1)
gold – Logarithm of gold price
gold2 – gold price (USD per troy ounce)
"""
##################
#Question 1
#Implementation
##################
gold=[5.264967387, 5.719262046, 6.420808929, 6.129616498, 
      5.927725706, 6.048931247, 5.888268354, 5.759847699, 
      5.907675246, 6.100812104, 6.079612778, 5.942326823, 
      5.949496062, 5.892362186, 5.840496298, 5.885603906, 
      5.951033101, 5.950772752, 5.960670232, 5.802994125, 
      5.683885843, 5.629669374, 5.631570141, 5.602266411, 
      5.735539506, 5.895283989, 6.014130718, 6.096837563, 
      6.403193331, 6.544472839, 6.770743551, 6.879715822, 
      7.110304209, 7.359798583, 7.41996794, 7.252216944, 7.143933509]

gold2=[193, 305, 615, 459, 375, 424, 361, 317, 368, 446, 
       437, 381, 384, 362, 344, 360, 384, 384, 388, 331, 294, 
       279, 279, 271, 310, 363, 409, 444, 604, 695, 872, 972, 
       1225, 1572, 1669, 1411, 1266]

lag = gold[:-1]
gold=[5.719262046, 6.420808929, 6.129616498, 5.927725706, 
      6.048931247, 5.888268354, 5.759847699, 5.907675246, 
      6.100812104, 6.079612778, 5.942326823, 5.949496062, 
      5.892362186, 5.840496298, 5.885603906, 5.951033101, 
      5.950772752, 5.960670232, 5.802994125, 5.683885843, 
      5.629669374, 5.631570141, 5.602266411, 5.735539506, 
      5.895283989, 6.014130718, 6.096837563, 6.403193331, 
      6.544472839, 6.770743551, 6.879715822, 7.110304209, 
      7.359798583, 7.41996794, 7.252216944, 7.143933509]

beta, alpha, r_value, p_value, std_err = stats.linregress(gold, lag)
print("beta = ", beta, "alpha = ",alpha)
print("R-Square = ", r_value**2)
print("P-value = ", p_value)

forecast_gold = np.exp(beta*gold[len(gold)-1]+alpha)
print("Forecasted gold price for 2015\n", forecast_gold)

plt.plot(gold2)
plt.grid()
plt.title("Gold Price Evolution from 1978 until 2014")
plt.xlabel("Period")
plt.ylabel("USD per troy ounce")
plt.show()

##################
#Question 2
#Implementation
##################
gold_file = r'jpy_gold_price.csv'
cur_gold_price = pd.read_csv(gold_file)
#print(cur_gold_price)
plt.plot(cur_gold_price['PRICE'])
plt.grid()
plt.title("Gold Price Evolution from 1978 to Date")
plt.xlabel("Period")
plt.ylabel("JPY per troy ounce")
plt.show()

series = pd.DataFrame(cur_gold_price, columns=['DATE','PRICE'])
series = series.set_index('DATE')

autocorrelation_plot(series)
plt.show()

model = ARIMA(series, order=(5,0,5))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# plot residual errors
residuals = pd.DataFrame(model_fit.resid)
residuals.plot()
residuals.plot(kind='kde')
plt.show()
print(residuals.describe())

print("\r\n\r\nForecatsed Gold Price in JPY\r\n",27*"=")
print(model_fit.forecast())
