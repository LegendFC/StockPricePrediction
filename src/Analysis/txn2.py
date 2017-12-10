from __future__ import division
import numpy as np
import pandas as pd
from collections import Counter


def getdatalabel(fileofdata,fileoflabel):
    
    data = pd.read_csv(fileofdata, sep="\t", index_col=None)
    price = pd.read_csv(fileoflabel, sep=",", index_col=None)
    
    sentiment_count = data.groupby(['date', 'sentiment']).size().reset_index(name='counts')
    subjectivity_count = data.groupby(['date', 'subjectivity']).size().reset_index(name='counts')
    
    for key, value in Counter(sentiment_count.date).items():
        if value != 3:
            data.drop(data[data.date == key].index, inplace=True)
    for key, value in Counter(subjectivity_count.date).items():
        if value != 3:
            data.drop(data[data.date == key].index, inplace=True)
    # reindex data
    data = data.reset_index(drop=True)
    
    # recount
    sentiment_count = data.groupby(['date', 'sentiment']).size().reset_index(name='counts')
    subjectivity_count = data.groupby(['date', 'subjectivity']).size().reset_index(name='counts')
    
    data_matrix = np.zeros((len(Counter(data.date).keys()), 8))
    
    data_matrix[:, 4] = data["numWords"].groupby(data.date).mean()[::-1]
    data_matrix[:, 5] = data["numSentences"].groupby(data.date).mean()[::-1]
    data_matrix[:, 6] = data["numNouns"].groupby(data.date).mean()[::-1]
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
        
    
    for i in range(len(price.Date)):
        if price.Date[i] not in set(data.date):
            price.drop(price[price.Date == price.Date[i]].index, inplace=True)
    
    y = [x for x in price.High if x > 0]
    
    
    price_date_set = set(price.Date)
    delete_row = []
    for i in range(len(data_matrix)):
        if sentiment_count.date[i*3] not in price_date_set:
            delete_row.append(i)
    
    
    # get X and Y
    X = np.delete(data_matrix, delete_row, 0)
    Y = y[:len(X)]
    
    return X,Y
    
