#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 01:15:47 2018

@author: abayomi


import quandl

quandl.ApiConfig.api_key = "wMzVVAMbc6y2yxCVGEGh"
mydata = quandl.get("BCIW/_SPXT")
print(mydata)
"""
import pandas as pd
import fix_yahoo_finance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

yf.pdr_override()

file = r'exchanges.csv'

exchanges = pd.read_csv(file)

"""
The line of code below retreive the date of 30 days ago
"""
startdate = (datetime.now() - timedelta(3650)).date()

"""
The line of code below retrieve the date of today.
"""
enddate = datetime.now().date()

indices = []

for l in range(0, len(exchanges)):
    pointer = l + 1
    if (pointer < 10):
        pointer = "0"+str(pointer)
    print(pointer,"  ->", exchanges['COUNTRY'][l].upper(),"--",exchanges['EXCHANGE'][l].upper())

def str_replace(sbjct, srch, rplc):
    if len(sbjct) == 0:
        return ''

    if len(srch) == 1:
        return sbjct.replace(srch[0], rplc[0])

    lst = sbjct.split(srch[0])
    reslst = []
    for s in lst:
        reslst.append(str_replace(s, srch[1:], rplc[1:]))
    return rplc[0].join(reslst);

def getdata(exc):
    all_index = yf.download(exc[0], start=startdate, end=enddate)
    
    if not all_index.empty:
        del all_index['Open']
        del all_index['High']
        del all_index['Low']
        del all_index['Close']
        del all_index['Volume']
        all_index.rename(columns={'Adj Close': exc[0].replace('^','')}, inplace=True)
        
    for j in range(1, len(exc)):
        pointer = exc[j].replace('^', '')
        setx = yf.download(exc[j], start=startdate, end=enddate)
        if not setx.empty:
            all_index[pointer] = setx['Adj Close']
            
    return all_index
        
    
def findInlist(xkey):
    if (xkey < len(exchanges) and xkey > -1):
        indices.append(exchanges['CODE'][xkey])
        return True
    else:
        return False
    
def plotmatrix(dmatrix):
    print("Monthly Return Correlation Coefficient Data Set\n")
    print(dmatrix.corr())
    plt.matshow(dmatrix.corr())
    

if __name__ == "__main__":
    lookup = True
    while lookup:
        userinput = input("Select any five of the stock exchanges show above in comma seperated list, using the index number:")
        ikey = userinput.split(",")
        kounter = 0
        for i in range(0, len(ikey)):
            rkey = int(ikey[i])-1
            if (rkey > -1 and findInlist(rkey) == True):
                kounter += 1
        if (kounter < len(ikey)):
            lookup = True
            print("One of the exchanges listed not found! Try again using the above listed exchanges only.")
        else:
            lookup = False
            data_matrix = getdata(indices)
            if not data_matrix.empty:
                plotmatrix(data_matrix)
            else:
                print("Empty dataset returned!")