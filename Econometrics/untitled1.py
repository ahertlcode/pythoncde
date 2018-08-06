#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 18:54:03 2018

@author: abayomi
"""

#print(df.tail())
sp.random.seed(12000)
v=1000		# v is the number of observations
v1=100		# we need to drop the first several observations
v2=v+v1		# sum of two numbers
alpha=(0.15,0.2)	# GARCH(1,1) coefficients alpha0 and alpha1
beta=0.2
errors=sp.random.normal(0,1,v2)
t=sp.zeros(v2)
t[0]=sp.random.normal(0,sp.sqrt(alpha[0]/(1-alpha[1])),1)
for i in range(1,v2-1):
 t[i]=errors[i]*sp.sqrt(alpha[0]+alpha[1]*errors[i-1]**2+beta*t[i-1]**2)


y=t[v1-1:-1] # drop the first v1 observations 
plt.title('GARCH (1,1) process')
x=range(v)
plt.plot(x,y)