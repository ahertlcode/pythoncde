#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 21:59:01 2018

@author: abayomi
"""

from	 numpy	import	random	,	histogram	,	arange	,	sqrt	,	exp	,	nonzero,	array	
from	 scipy.optimize	import	leastsq	
import pylab	
if	__name__	==	'__main__':
    n	=	1000
    isi=random.exponential(0.1	,	size=n)
    db	=	0.01	
    bins	 =	arange	(0	,1.0	,	db)
    h	=	histogram(isi,bins)[0]
    p	=	h.astype(float)/n/db	
    #print(bins)
    """
	#	Function	to	be	fit	
	#	x:	independent	variable	
	#	p:	tuple	of	parameters	
    """
    #fitfunc	=	lambda	p,x:exp(-x/p[0])/p[0]
    fitfunc = lambda p,x:exp(-x/p[0])/p[0]
    #	Standard	form,	here	err	is	absolute	error	
    errfunc=	lambda	p,	x	,	y	,	err	:	(y	-	fitfunc	(p,	x))/err	
    #	Initial	values	for	fit	parameters
    initialFitP	=	array([0.2])	
    """
    #	Hist	count less than four has poor estimate of the weight
    #	Don't use in the fitting process	
    """
    idx	=	nonzero(h>4)	
    out	=	leastsq(	errfunc,	initialFitP,	args=(	bins[idx]	+0.01/2	,	p[idx]	,p[idx]	/sqrt(h[idx])))
    l1	=	"Actual Data Points"
    pylab.errorbar(	bins[idx],p[idx],	yerr=p[idx]/sqrt(h[idx]),	fmt='ko',	label=l1,	color='red'	)
    l2	=	"Best Fit"
    pylab.plot(bins,fitfunc((out[0],),bins),'b--',lw=2,label=l2	)
    pylab.legend()
    pylab.show()	