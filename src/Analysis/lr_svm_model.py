from __future__ import division
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
from sklearn import datasets, svm, cross_validation, tree, preprocessing, metrics
import sklearn.ensemble as ske
from numpy import genfromtxt
import csv
import re
from collections import Counter
from sklearn import linear_model
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from sklearn import neural_network
from sklearn.svm import SVR
from collections import OrderedDict 

# load tweet data and price data
# from 12/01/2016 to 11/30/2017
data = pd.read_csv('TXN_data.txt', sep="\t", index_col=None)
price = pd.read_csv('TXN_price.txt', sep="\t", index_col=None)

# summarize everyday sentiment and subjectivity statistics or counts
sentiment_count = data.groupby(['date', 'sentiment']).size().reset_index(name='counts')
subjectivity_count = data.groupby(['date', 'subjectivity']).size().reset_index(name='counts')


# delete missing values
# those dates that have less than 3 kinds of sentiment and subjectivity 
for key, value in Counter(sentiment_count.date).iteritems():
    if value != 3:
        data.drop(data[data.date == key].index, inplace=True)
for key, value in Counter(subjectivity_count.date).iteritems():
    if value != 3:
        data.drop(data[data.date == key].index, inplace=True)
# reindex data
data = data.reset_index(drop=True)


# recount sentiment and subjectivity
sentiment_count = data.groupby(['date', 'sentiment']).size().reset_index(name='counts')
subjectivity_count = data.groupby(['date', 'subjectivity']).size().reset_index(name='counts')


# plan to extract some data for X
data_matrix = np.zeros((len(Counter(data.date).keys()), 8))


# mean of numWords
data_matrix[:, 4] = data["numWords"].groupby(data.date).mean()[::-1]
# mean of numSentences
data_matrix[:, 5] = data["numSentences"].groupby(data.date).mean()[::-1]
# mean of numNouns
data_matrix[:, 6] = data["numNouns"].groupby(data.date).mean()[::-1]
# number of tweets
data_matrix[:, 7] = np.array([i[1] for i in sorted(Counter(data.date).items(), reverse=True)])


for i in range(len(data_matrix)):
    # negative sentiment ratio
    data_matrix[i, 0] = sentiment_count['counts'][i*3] / data_matrix[i, 7]
    # positive sentiment ratio
    data_matrix[i, 1] = sentiment_count['counts'][i*3+2] / data_matrix[i, 7]
    # objective ratio
    data_matrix[i, 2] = subjectivity_count['counts'][i*3+1] / data_matrix[i, 7]
    # subjective ratio
    data_matrix[i, 3] = subjectivity_count['counts'][i*3+2] / data_matrix[i, 7]
    

# delete some price records according to those dates deleted in data
for i in range(len(price.Date)):
    if price.Date[i] not in set(data.date):
        price.drop(price[price.Date == price.Date[i]].index, inplace=True)

# delete dates in data when no stock price that day
price_date_set = set(price.Date)
delete_row = []
for i in range(len(data_matrix)):
    if sentiment_count.date[i*3] not in price_date_set:
        delete_row.append(i)


# get X and Y
X = np.delete(data_matrix, delete_row, 0)
# Y is high price
Y = [x for x in price.High if x > 0][:len(X)]


# add interaction
# positive negative sentiment interaction
X = np.insert(X, 8, X[:, 0]*X[:, 1], 1)

# scale X
X = scale(X)


# split to training and testing data
ratio = 0.6
X_train = X[:int(ratio*len(X)), :]
X_test = X[int(ratio*len(X)):, :]
Y_train = Y[:int(ratio*len(X))]
Y_test = Y[int(ratio*len(X)):]



# construct model, make prediction and plot trajectories
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 20))
# make a little extra space between the subplots
fig.subplots_adjust(hspace=0.5)



reg = linear_model.LinearRegression()
yr = reg.fit(X_train, Y_train).predict(X)
print "MSE from Linear Regression: ", sum((yr[int(ratio*len(X)):] - Y_test)**2) / len(Y_test)


svr = SVR(kernel='rbf', C=1e5, gamma=0.0001)
#svr = SVR(kernel='poly', C=1e3, degree=2)
ysvr = svr.fit(X_train, Y_train).predict(X)
print "MSE from SVM Regression: ", sum((ysvr[int(ratio*len(X)):] - Y_test)**2) / len(Y_test)




t = np.arange(0, len(X), 1)

s1 = Y
s2 = yr
s3 = ysvr


ax1.plot(t, s1, label='True price')
ax1.plot(t, s2, label='Predicted price')
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Price')
ax1.set_title('Linear Regression')
ax1.legend()
ax1.grid(True)
ax2.plot(t, s1, label='True price')
ax2.plot(t, s3, label='Predicted price')
ax2.set_xlabel('Date')
ax2.set_ylabel('Stock Price')
ax2.set_title('SVM Regression with rbf Kernel')
ax2.legend()
ax2.grid(True)
fig.savefig('modelresult.png')   # save the figure to file
plt.close(fig)


