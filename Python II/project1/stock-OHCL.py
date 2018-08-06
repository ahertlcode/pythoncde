# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pandas_datareader import data as pdr
import pandas as pd
import fix_yahoo_finance as yf
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

yf.pdr_override()


"""
point the file aurgment to the csv file containing tickers available on NASDAQ
whose price and historical data can be fetched from yahoo finance. 
"""
file = r'tickers.csv'
"""
The line of code below retreive the date of 30 days ago
"""
startdate = (datetime.now() - timedelta(30)).date()

"""
The line of code below retrieve the date of today.
"""
enddate = datetime.now().date()

"""loading the content of the csv file with pandas"""
tickers = pd.read_csv(file)

"""
This function look through the tickers in the csv file to find the ticker entered
by the user if it available.
"""
def findInlist(stock):
    counter = 0
    for i in range(0, len(tickers)):
        #compare the enter tickers with the tickers in the csv file 
        if (stock == tickers['ticker'][i]):
            counter += 1
    if counter > 0:
        return True
    else:
        return False
            

"""
this function fetch data from yahoo finance using the supplied ticker with the 
specified startdate and enddate using the pandas_datareader library
"""      
def getdata(ticker,sdate,edate):
    data = pdr.get_data_yahoo(ticker, start=sdate, end=edate)
    return data

"""
This function retrieve the date and adjusted closing price columns
of the pandas data frame and return them has lists
"""
def split_data_pt(data):
    x = []
    y = []
    for i in range(len(data)):
        x.append( str(data.index[i]) )
        y.append( data.loc[:, "Adj Close"][i] )
    return x, y

def plotgraph(ticker, x0, y):
    x = list(range(len(x0)))
    
    #f1 = interp1d(x, y)
    f2 = interp1d(x, y, kind='cubic')

    # Array with points in between min(x) and max(x) for interpolation
    x_interp = np.linspace(min(x),max(x),num=np.size(x))

    # Plot graph with interpolation
    plt.plot(x, y, 'o', x_interp, f2(x_interp), '-')
    plt.legend(['Raw Market Data', 'Quadratic Interpolation'], loc='best')
    plt.title(ticker+" Graph of Adjust Closing Price from "+str(startdate)+" to "+str(enddate))
    plt.show()  
   

"""
This block of code accept user input and check for its validity against providers
tickers by the system
"""
lookup = True

while lookup:
    symbol = (input("Enter a ticker/stock symbol:")).upper()
    if (findInlist(symbol) == True):
        lookup = False
        market_data = getdata(symbol,startdate, enddate)
        if(len(market_data)>0):
            x_axis, y_axis = split_data_pt(market_data)
            plotgraph(symbol, x_axis, y_axis)
        else:
            lookup = True
            print("Data Point Not Found for Selected Stock ticker, choose another one.")
    else:
        print("Ticker not found! Please try a different stock ticker/symbol")
        lookup = True
        


