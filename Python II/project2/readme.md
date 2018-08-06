Readme file
===========

This application was design using Python 3.6.4 with spyder in the anaconda IDE on an `Ubuntu 16.04 64 bit system`. But it show run on any system runing python 2.7+ has no python3 specific code or functions were used.

libraries
----------

The various libraries used will have to be installed using the “pip install libraryname” command in other for the application to run without any error.

The following were the libraries used:
pandas, pandas_datareader,

    `fix_yahoo_finance`, `datetime`

from where

    `datetime` and  `timedelta`

were imported and used,

    `numpy`, `matplotlib.pyplot` and `scipy.interpolate`

from where

    `interp1d`

imported and used also.

User Input
----------

The input must be valid stock suffixes on various market index available on stock exchanges all over the world. The application provide a list of such common market indices like the popular S&P 500, DOW JONES INDEX for USA, CNXNIFTY for India, HANGSENG Index for Hong Kong for guidance

How to Run the Application
--------------------------

A python shebang is include at the top of the script and thus can be ran from the commandline by specifying the python version and the path to the environment where the python executable is located.