from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import statsmodels.api as sm
import numpy as np
import pandas as pd

yf.pdr_override()


def get_avg(dataset):
    return sum(dataset, 0)/len(dataset)


def get_daily_ret(dataset):
    daily_returns = []
    daily_returns.append(0)
    for ptr in range(0, len(dataset)):
        if ptr < len(dataset)-1:
            daily_returns.append(
                (dataset['Adj Close'][ptr+1] -
                    dataset['Adj Close'][ptr])/
                    dataset['Adj Close'][ptr])
    return daily_returns

jpm_data = pdr.get_data_yahoo("JPM", "2015-04-01", "2015-06-25", asobject=True, adjusted=True)

snp500 = pdr.get_data_yahoo("^GSPC", "2015-04-01", "2015-06-25", asobject=True, adjusted=True)

#solution1
average_stock_value = get_avg(jpm_data['Adj Close'])
print("Average Stock Value: ", '{:04.4f}'.format(average_stock_value))

#solution2
vola = pd.DataFrame(get_daily_ret(jpm_data)).std()
print("Stock Price Volatility: ", vola[0])
print("Annualized Volatility: ", np.sqrt(252)*vola[0])

#solution3
daily_returns = get_daily_ret(jpm_data)
print("DAILY RETURNS FOR JPMORGAN CHASE & CO\r\n", 37*"=","\r\n")
print(pd.DataFrame(daily_returns, columns=['Daily Returns']))

#regression model
snp = np.log(snp500['Adj Close'])
jpm = np.log(jpm_data['Adj Close'])
snp = sm.add_constant(snp)
model = sm.OLS(jpm, snp)
result = model.fit()
print(result.summary())