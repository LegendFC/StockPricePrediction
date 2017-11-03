import pandas_datareader as pdr
from datetime import datetime

google = pdr.get_data_yahoo(symbols='GOOG', start=datetime(2017, 1, 1), end=datetime(2017, 10, 1))
print(google)


g = pdr.get_data_yahoo(symbols='GOOG')
print(g)