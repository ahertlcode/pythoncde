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

    `numpy`, `matplotlib.pyplot` and `scipy.stats`

all this libraries were used are all required and must be install if they are not already on the system.

User Input
----------

This application does not expects any input from users as the data it depends on are predetermined and downloaded directly from yahoo finance hence the need to have a working internet connection for the application to access the data needed for smooth operation from yahoo finance online. A csv file that contains all the indices considered in application is contained in the root directory of the application named indexes.csv this file also must be kept intact and must not be altered.

How to Run the Application
--------------------------

A python shebang is include at the top of the script and thus can be ran from the commandline by specifying the python version and the path to the environment where the python executable is located.