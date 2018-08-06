from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import statsmodels.api as sm
import numpy as np
import pandas as pd

yf.pdr_override()

#download JPMorgan Chase & Co Price and S&P 500 index from yahoo finance.
jpm_data = pdr.get_data_yahoo("JPM", "2015-03-25", "2015-06-25", asobject=True, adjusted=True)
snp500 = pdr.get_data_yahoo("^GSPC", "2015-03-25", "2015-06-25", asobject=True, adjusted=True)

# joining the closing prices of the two datasets
monthly_prices = pd.concat([jpm_data['Close'], snp500['Close']], axis=1)
monthly_prices.columns = ['JPM', '^GSPC']

# check the head of the dataframe
print(monthly_prices.head())

# calculate monthly returns
monthly_returns = monthly_prices.pct_change(1)
clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row

# split dependent and independent variable
X = clean_monthly_returns['^GSPC']
y = clean_monthly_returns['JPM']

# Add a constant to the independent value
X1 = sm.add_constant(X)

# make regression model
model = sm.OLS(y, X1)

# fit model and print results
results = model.fit()
print(results.summary())