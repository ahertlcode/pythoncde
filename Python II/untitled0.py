#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 22:35:08 2018

@author: abayomi
"""

# Plot a line graph of combine yearly returns
    combine_returns = pd.DataFrame(columns=['YEAR','DJIA DEMO', 
                                            'DJIA REP', 'S&P 500 DEMO', 
                                            'S&P 500 REP'])
    
    # Make the year column the dataframe index before plotting.
    combine_returns = combine_returns.set_index('YEAR')
    
    combine_returns['YEAR'] = rep_snp500['year']
    combine_returns['DJIA DEMO'] = demo_dow['returns']
    combine_returns['DJIA REP'] = rep_dow['returns']
    combine_returns['S&P 500 DEMO'] = demo_snp500['returns']
    combine_returns['S&P 500 REP'] = rep_snp500['returns']    
      
    combine_returns['DJIA DEMO'] = combine_returns.fillna(combine_returns['DJIA DEMO'].mean())
    combine_returns['DJIA REP'] = combine_returns.fillna(combine_returns['DJIA REP'].mean())
    combine_returns['S&P 500 DEMO'] = combine_returns.fillna(combine_returns['S&P 500 DEMO'].mean())
    
    print("\r\nCombine Returns\r\n===============\r\n", combine_returns)
    
    combine_returns.plot()