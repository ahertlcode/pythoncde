#!/usr/bin/env python3
"""Final Project: The Misbehavior of Markets

# =============================================================================
# Date Created | Author |
# Friday May  18 11:20:47 2018 | Abayomi Apetu |
#
# Code uses Python 2.7+
#
# -- Project Description
#1, Write a python program(s) to download end-of-day data last 25
#   years the major global stock market indices from Google Finance,
#   Yahoo Finance, Quandl, CityFALCON, or another similar source.
#
#2, It is a common assumption in quantitative finance that stock
#   returns follow a normal distribution whereas prices follow a
#   lognormal distribution For all these indices check how closely
#   price movements followed a log-normal distribution.
#
#3, Verify whether returns from these broad market indices followed
#   a normal distribution?
#
#4, For each of the above two parameters (price movements and stock
#   returns) come up with specific statistical measures that clearly
#   identify the degree of deviation from the ideal distributions.
#   Graphically represent the degree of correspondence.
#
#5, One of the most notable hypothesis about stock market behavior
#   is the “Efficient market hypothesis” which also internally assume
#   that market price follows a random-walk process. Assuming that
#   Stock Index prices follow a geometric Brownian motion and hence
#   index returns were normally distributed with about 20% historical
#   volatility, write a program sub-module to calculate the probability
#   of an event like the 1987 stock market crash happening ? Explain in
#   simple terms what the results imply.
#
#6, What does "fat tail" mean? Plot the distribution of price movements
#   for the downloaded indices (in separate subplot panes of a graph) and
#   identify fat tail locations if any.
#
#7, It is often claimed that fractals and multi-fractals generate a more
#   realistic picture of market risks than log-normal distribution.
#   Considering last 10 year daily price movements of NASDAQ, write a program
#   to check whether fractal geometrics could have better predicted stock
#   market movements than log-normal distribution assumption. Explain your
#   findings with suitable graphs.
#
# -*- coding: utf-8 -*-
"""


import pandas as pd
import fix_yahoo_finance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

class Behaviour:

    def __init__(self):
        self.startdate = ""
        self.enddate = ""
        self.dret = []
        self.returns_tab = pd.DataFrame()

    def get_market_indices(self, data):
        """End-of-day Data Downloads

        This function downloads the end-of-day data last 25
        years the major global stock market indices from
        Yahoo Finance"""

        #The line of code below retreive the date of 25 years ago
        backdate = 365 * 25
        self.startdate = (datetime.now() - timedelta(backdate)).date()

        #The line of code below retrieve the date of today.
        self.enddate = datetime.now().date()

        #Creating a pandas DataFrame to hold the downloaded data
        market_indices = pd.DataFrame()
        for ftr in  range(0, len(data)):

            #Actual downloads is done on this line
            mdata = yf.download(data['CODE'][ftr],
                start=self.startdate, end=self.enddate)

            #This line append the 'Adj Close' column of the downloaded
            # data to the DataFrame declared
            market_indices[data['INDEX'][ftr]] = mdata['Adj Close']

        #The pandas DataFrame is returned
        return market_indices

    def daily_return(self, indexes, data):

        self.returns_tab = data
        for itr in range(0, len(indexes)):
            self.dret.clear()
            self.dret.append(0)
            for ptr in range(0, len(data[indexes['INDEX'][itr]])):
                if ptr < len(data[indexes['INDEX'][itr]])-1:
                    self.dret.append(
                        (data[indexes['INDEX'][itr]][ptr+1] - data[indexes['INDEX'][itr]][ptr])/
                            data[indexes['INDEX'][itr]][ptr]
                    )
            self.returns_tab[indexes['INDEX'][itr]] = self.dret
        return self.returns_tab

    def do_log_normal(self, data, dcolor, cod):
        """Log-normal Distribution

        This function does a log-normal fit for time series movement"""
        s, loc, scale = stats.lognorm.fit(data, floc=0)

        estimated_mu = np.log(scale)
        estimated_sigma = s

        plt.hist(data, bins=50, normed=True, color=dcolor, alpha=0.75)
        xmin = data.min()
        xmax = data.max()
        x = np.linspace(xmin, xmax, 100)
        pdf = stats.lognorm.pdf(x, s, scale=scale)
        plt.plot(x, pdf, 'm')

        plt.suptitle('Log-normal Districution Curve '+cod)
        plt.show()
        print("Mean of the Distribution: ", estimated_mu)
        print("Standard Deviation of the Distribution: ", estimated_sigma)

    def do_normal_dist(self, data, codx):
        """Normal Probability Distribution

        This method verify whether returns from these broad
        market indices followed a normal distribution
        """
        #this is a fitting indeed
        mean = np.mean(data) #data.mean()
        std = np.std(data) #data.std()
        variance = np.var(data) #data.var()


        #use this to draw histogram of your data
        plt.hist(data, normed=True)
        xmin = data.min()
        xmax = data.max()
        x = np.linspace(xmin, xmax, 100)
        fit = stats.norm.pdf(x, mean, std)
        plt.plot(x, fit,'r')
        plt.suptitle("Normal Districution Curve for "+codx)
        plt.show()
        print("Mean of Returns: ", mean)
        print("Standard Deviation of Returns: ", std)
        print("Variance of Returns: ", variance)

    def main(self):
        """
        The main function of the application

        This solution begin to execute from here.
        step 1: Downloading the end-of-day data last 25 years"""
        #index_list = mkt.get_market_indices(_indexes_)

        #replace all nan value with the mean of the particular index
        data['DJIA'] = data['DJIA'].fillna(data['DJIA'].mean())
        data['S&P500'] = data['S&P500'].fillna(data['S&P500'].mean())
        data['NASDAQ'] = data['NASDAQ'].fillna(data['DJIA'].mean())
        data['DAX'] = data['DAX'].fillna(data['DAX'].mean())
        data['FTSE100'] = data['FTSE100'].fillna(data['FTSE100'].mean())
        data['HSI'] = data['HSI'].fillna(data['HSI'].mean())
        data['KOSPI'] = data['KOSPI'].fillna(data['KOSPI'].mean())
        data['NIFTY50'] = data['NIFTY50'].fillna(data['NIFTY50'].mean())
        data.set_index('Date', inplace=True)

        """Step 2:

        Log-normal Distribution price movement check all the indices had
        been stored in csv file that is been read with pandas into _indexes_
        DataFrame"""
        #Dow Jones
        self.do_log_normal(data['DJIA'], 'b', 'DOW JONES')
        #S&P 500
        self.do_log_normal(data['S&P500'], 'r', 'S&P 500')
        #NASDAQ
        self.do_log_normal(data['NASDAQ'], 'y', 'NASDAQ')
        #DAX
        self.do_log_normal(data['DAX'], 'g', 'DAX')
        #FTSE100
        self.do_log_normal(data['FTSE100'], 'k', 'FTSE 100')
        #HSI
        self.do_log_normal(data['HSI'], 'c', 'HSI')
        #KOSPI
        self.do_log_normal(data['KOSPI'], 'm', 'KOSPI')
        #NIFTY50
        self.do_log_normal(data['NIFTY50'], 'y', 'NIFTY 50')

        """Step 3:

        To verify if returns follow normal distribution
        We have to calculate the daily returns for all the
        indices"""
        returns = self.daily_return(_indexes_, data)

        #Dow Jones
        self.do_normal_dist(returns['DJIA'], 'DOW JONES')
        #S&P 500
        self.do_normal_dist(returns['S&P500'], 'S&P 500')
        #NASDAQ
        self.do_normal_dist(returns['NASDAQ'], 'NASDAQ')
        #DAX
        self.do_normal_dist(returns['DAX'], 'DAX')
        #FTSE100
        self.do_normal_dist(returns['FTSE100'], 'FTSE 100')
        #HSI
        self.do_normal_dist(returns['HSI'], 'HSI')
        #KOSPI
        self.do_normal_dist(returns['KOSPI'], 'KOSPI')
        #NIFTY50
        self.do_normal_dist(returns['NIFTY50'], 'NIFTY 40')

        """Step 4:

        For each of the above two parameters (price movements and stock
        returns) come up with specific statistical measures that clearly
        identify the degree of deviation from the ideal distributions.
        Graphically represent the degree of correspondence."""
        print("\nStudent T-test for Price Movement\n", 35*"=","\n")
        pmove = stats.ttest_1samp(data, data.mean())
        print(pmove)
        print("\nStudent T-test for Returns\n",30*"=","\n")
        retdis = stats.ttest_1samp(returns, returns.mean())
        print(retdis)
        plt.plot(pmove)
        plt.suptitle("Graphically represent the degree of correspondence between price movement")
        plt.show()
        plt.plot(retdis)
        plt.suptitle("Graphically represent the degree of correspondence between returns")
        plt.show()





if __name__ == "__main__":
    # pylint: disable=C0103
    yf.pdr_override()

    file_in = r'indexes.csv'

    _indexes_ = pd.read_csv(file_in)

    mkt = Behaviour()
    
    data = mkt.get_market_indices(_indexes_)

    mkt.main()
