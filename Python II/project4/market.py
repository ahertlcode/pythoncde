#!/usr/bin/env python3
"""Project 4: How Do Markets React to Republicans and Democrats?

# =============================================================================
# Date Created | Author |
# Tue May  16 01:15:47 2018 | Abayomi Apetu |
#
# Code uses Python 2.7+
#
# -- Project Description
# -Create a csv file with a list of all presidents,
#  their parties from 1920 onwards
# -Using Pandas load the .csv file into a Pandas dataframe.
# -Download data from an appropriate financial website
#  such as Google Finance, Yahoo Finance, Quandl, CityFALCON,
#  or another similar source.
# -Calculate yearly returns for both the downloaded indices
#  from 1920 onwards
# -Segregate returns in terms of Presidency – i.e. stock market
#  returns during Democratic and Republican years
# -Calculate measures of central tendency (mean return, median
#  return, variance of returns) for each of the two groups.
# -Represent the findings through suitable comparative graphical studies
"""

# -*- coding: utf-8 -*-



from datetime import datetime
import pandas as pd
import fix_yahoo_finance as yf
import matplotlib.pyplot as plt


class Market:
    """ Market Reaction to Republicans/Democratics

    This application is written has a mini project in
    python II a course offered in pursuit of an M.Sc FE
    from the WQU. The application was written to test the
    effects various political system has on the market"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.dow_index = pd.DataFrame()
        self.snp500_index = pd.DataFrame()
        self.daily_returns = []
        self.years = []
        self.yreturns = []
        self.returns = []
        self.pres_ret = []
        self.party = []


    def get_dow_data(self):
        """ Dow Jones Industrial Average

        This function downloads the DJI index from yahoo finance
        using startdate='1920-01-01' and enddate as current date
        and returned the same as a pandas DataFrame """
        self.dow_index = yf.download('^DJI', start=startdate, end=enddate)
        return self.dow_index['Adj Close']

    def get_snp500_data(self):
        """S&P 500 INDEX

        This function downloads the S&P 500 index from yahoo finance
        using startdate='1920-01-01' and enddate as current date
        and returned the same as a pandas DataFrame """
        self.snp500_index = yf.download('^GSPC', start=startdate, end=enddate)
        return self.snp500_index['Adj Close']

    def calc_daily_returns(self, dataset):
        """Daily Returns Calculator

        This function calculates daily returns it accept
        dataset a pandas DataFrame comprising of the Adj Close
        columns of the DataFrame"""
        self.daily_returns.clear()
        self.daily_returns.append(0)
        for ptr in range(0, len(dataset)):
            if ptr < len(dataset)-1:
                self.daily_returns.append(
                    (dataset['Adj Close'][ptr+1] -
                     dataset['Adj Close'][ptr])/
                    dataset['Adj Close'][ptr])
        return self.daily_returns

    def get_years(self, dataset):
        """Year Formulator

        This is an helper function that return in a list
        years of trade given the trade date column of
        the pandas DataFrame"""
        self.years.clear()
        for ptr in range(0, len(dataset)):
            if ptr < len(dataset):
                self.years.append(int(str(dataset['Date'][ptr]).split("-")[0]))
        return self.years

    def do_yearly_returns(self, dataset):
        """Yearly Returns Calculator

        This function given dataset as a pandas DataFrame
        with the year column introduce by the helper function
        and the already calculated daily return also added
        to the pandas DataFrame calculates the yearly return
        that is returned as a list"""
        self.yreturns.clear()
        ptr1 = 0
        for ptr2 in range(0, len(dataset)):
            if dataset['year'][ptr1] == dataset['year'][ptr2]:
                self.returns.append(dataset['daily returns'][ptr2])
            else:
                calc = sum(self.returns) #/len(returns_)
                self.yreturns.append({
                    "year" : dataset['year'][ptr1],
                    "returns" : calc
                })
                self.returns.clear()
                ptr1 = ptr2
        return self.yreturns

    def get_party(self, dataset, lookup):
        """Party Segregator

        This function accepts dataset a pandas DataFrame
        of presidency read from csv and returned a list
        of python dictionary containing year and the
        political party of the president that ruled that
        year."""
        self.party.clear()
        for ptr1 in range(0, len(dataset)):
            dyear1 = int(dataset['Start'][ptr1].split(" ")[2])
            dyear2 = int(dataset['End'][ptr1].split(" ")[2])
            if dyear1 >= 1920 and dataset['Party'][ptr1] == lookup:
                self.party.append({
                    "year-start" : dyear1,
                    "year-end" : dyear2,
                    "party" : lookup
                })
        return self.party

    def split_returns_by_presidency(self, rets, presidency):
        """ Yearly Return Splitted

        This function filter out the yearly returns
        during the presideny of a particular political
        party"""
        self.pres_ret.clear()
        for ptr in range(0, len(presidency)):
            for ptr2 in range(0, len(rets)):
                if (rets['year'][ptr2] >= presidency['year-start'][ptr]
                        and rets['year'][ptr2] < presidency['year-end'][ptr]):
                    self.pres_ret.append({
                        "year" : rets['year'][ptr2],
                        "returns" : rets['returns'][ptr2]
                    })
        return self.pres_ret



if __name__ == "__main__":
    # pylint: disable=C0103
    yf.pdr_override()

    mkt_ = Market()

    file = r'presidents.csv'

    # read the presidency csv file
    presidents = pd.read_csv(file)

    #set start date
    startdate = "1920-01-01"

    #set the end date as today
    enddate = datetime.now().date()

    # Create an empty pandas DataFrame
    df_dji = pd.DataFrame(columns=['Adj Close', 'daily returns', 'year'])

    # Retrieve the Adj Close columns of the DJIA index from yahoo finance.
    df_dji['Adj Close'] = mkt_.get_dow_data()

    # Reset the DataFrame index so that the Date column will be accessible
    # and a sequencial index will be used instead.
    df_dji = df_dji.reset_index()

    # Calculate daily returns from the DJIA index retrieved
    df_dji['daily returns'] = mkt_.calc_daily_returns(df_dji)
    df_dji['year'] = mkt_.get_years(df_dji)

    # Calculate DJIA yearly returns
    dow_yearly_ret = mkt_.do_yearly_returns(df_dji)

    # Create an empty pandas DataFrame
    df_snp = pd.DataFrame(columns=['Adj Close', 'daily returns', 'year'])

    # Retrieve the Adj Close columns of the S&P 500 index from yahoo finance
    df_snp['Adj Close'] = mkt_.get_snp500_data()

    # Reset the DataFrame index so that the Date column will be accessible
    # and a sequencial index will be used instead.
    df_snp = df_snp.reset_index()
    
    # Calculate daily returns from the S&P 500 index retrieved
    df_snp['daily returns'] = mkt_.calc_daily_returns(df_snp) #for S&P 500
    df_snp['year'] = mkt_.get_years(df_snp) #for yearly returns calculation of S&P 500

    # Calculate S&P 500 yearly returns
    snp_yearly_ret = mkt_.do_yearly_returns(df_snp)

    #load the yearly return into pandas DataFrame
    df_dow_yearly = pd.DataFrame(dow_yearly_ret, columns=['year', 'returns'])
    df_snp_yearly = pd.DataFrame(snp_yearly_ret, columns=['year', 'returns'])

    #get presidency to aid data seggregation
    republicans = pd.DataFrame(mkt_.get_party(presidents, 'Republican'))
    democrats = pd.DataFrame(mkt_.get_party(presidents, 'Democratic'))

    #yearly returns by presidency
    rep_dow = pd.DataFrame(mkt_.split_returns_by_presidency(
        df_dow_yearly,
        republicans
    ))


    rep_snp500 = pd.DataFrame(mkt_.split_returns_by_presidency(
        df_snp_yearly,
        republicans
    ))

    demo_dow = pd.DataFrame(mkt_.split_returns_by_presidency(
        df_dow_yearly,
        democrats
    ))

    demo_snp500 = pd.DataFrame(mkt_.split_returns_by_presidency(
        df_snp_yearly,
        democrats
    ))
    
    # Display tables of various yearly returns and their measures
    # of central tendencies mean, median, variance.
    print("\r\nDow Jones During Democratics\r\n",
          "=============================\r\n",
          demo_dow,
          "\r\n=============================\r\n\r\nMean: ",
          demo_dow['returns'].mean(),
          "\r\n\r\nMedian: ", demo_dow['returns'].median(),
          "\r\n\r\nVariance: ", demo_dow['returns'].var())

    print("\r\nS&P 500 During Democratics\r\n",
          "=============================\r\n",
          demo_snp500,
          "\r\n=============================\r\n\r\nMean: ",
          demo_snp500['returns'].mean(),
          "\r\n\r\nMedian: ", demo_snp500['returns'].median(),
          "\r\n\r\nVariance: ", demo_snp500['returns'].var())

    print("\r\nDow Jones During Republicans\r\n",
          "=============================\r\n",
          rep_dow,
          "\r\n=============================\r\n\r\nMean: ",
          rep_dow['returns'].mean(),
          "\r\n\r\nMedian: ", rep_dow['returns'].median(),
          "\r\n\r\nVariance: ", rep_dow['returns'].var())

    print("\r\nS&P 500 During Republicans\r\n",
          "=============================\r\n",
          rep_snp500,
          "\r\n=============================\r\n\r\nMean: ",
          rep_snp500['returns'].mean(),
          "\r\n\r\nMedian: ", rep_snp500['returns'].median(),
          "\r\n\r\nVariance: ", rep_snp500['returns'].var())


    # Collate the central tendencies to plot a barchar
    barplot = pd.DataFrame({
        "mean":{
            "DJIA_REP": rep_dow['returns'].mean(),
            "S&P_REP": rep_snp500['returns'].mean(),
            "DJIA_DEM": demo_dow['returns'].mean(),
            "S&P_DEM": demo_snp500['returns'].mean()
            },
        "media": {
            "DJIA_REP": rep_dow['returns'].median(),
            "S&P_REP": rep_snp500['returns'].median(),
            "DJIA_DEM": demo_dow['returns'].median(),
            "S&P_DEM": demo_snp500['returns'].median()
            },
        "variance": {
            "DJIA_REP": rep_dow['returns'].var(),
            "S&P_REP": rep_snp500['returns'].var(),
            "DJIA_DEM": demo_dow['returns'].var(),
            "S&P_DEM": demo_snp500['returns'].var()
            }
        })

    #Display the table of measure of central tendencies
    print(barplot)
    
    # Combine the yearly returns per presidency into on DataFrame 
    df_combined = pd.DataFrame()
    df_combined['REP_DOW'] = rep_dow.set_index(['year'])['returns']
    df_combined['REP_SNP500'] = rep_snp500.set_index(['year'])['returns']
    df_combined['DEM_DOW'] = demo_dow.set_index(['year'])['returns']
    df_combined['DEM_SNP500'] = demo_snp500.set_index(['year'])['returns']    
    
    """
    frames = [rep_dow, rep_snp500, demo_dow, demo_snp500]
    df_final = pd.concat(frames)
    print(df_final)
    
    
    fig = plt.figure()
    for frame in []:
        plt.plot(frame['year'], frame['returns'])
        
    plt.show()
    """

    # Ploting the barchart from the pandas DataFrame
    barplot.plot.bar()
    
    # Ploting barchat for yearly returns
    df_combined.plot.bar()
