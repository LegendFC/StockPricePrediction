#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 20:33:24 2017
@author: ericd
"""

import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

random.seed(0)


def getDataframe(filePath):
    dataframe = pd.read_csv(filePath, sep=",", index_col=None)
    y = dataframe['Close']
    x = dataframe.drop(['Close','Volume'], axis=1)
    return x, y

def applyminmax(dataframe):
    x = np.array(dataframe)
    amax=x.max(axis = 0)
    amin=x.min(axis = 0)
    dataframe = (dataframe-amin)/(amax-amin) 
    return dataframe

def rand(a, b):
    return (b - a) * random.random() + a


def make_matrix(m, n, fill=0.0):
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)

def compute_mse(predicted, test):
    count = 0
    for i in range(len(test)):
        count += (predicted[i]-test[i])**2
    mse=sum(count)/len(test)
    print ('MSE: ', mse)


class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0
        self.hidden_n = 0
        self.output_n = 0
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        self.input_weights = []
        self.output_weights = []
        self.input_correction = []
        self.output_correction = []

    def setup(self, ni, nh, no):
        self.input_n = ni + 1
        self.hidden_n = nh
        self.output_n = no
        
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # set weight
        self.input_weights = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)
        # randomly get data
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = rand(-2.0, 2.0)
        
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        # input layer
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # hidden layer calculation
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total)
        # output layer calculation
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total)
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        self.predict(case)
        # get output layer error
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error
            
        # get hidden layer error
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error
        # update output weights
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h] 
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # update input weights
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change

        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit=10000, learn=0.05, correct=0.1):
        for j in range(limit):
            error = 0.0
            for i in range(len(cases)):
                case = cases[i]
                label = labels[i]
                error += self.back_propagate(case, label, learn, correct)

    def test(self):
        
        pat_x = []
        labels = []
        cases = []
        test_x, test_y = getDataframe('TXN_price.txt')
        predict_list = []
        labels_train,cases_train,labels_test,cases_test=[],[],[],[]
        for i in range(len(test_y)):
            pat_x=test_x.values[i][1:]
            labels.append([test_y.values[i]])
            cases.append(pat_x)
        
        labels[:]=labels[1:]
        cases[:]=cases[:-1]
        
        #train part
        
        labels_train[:] = labels[1::2] #even index to get train data
        cases_train[:] = cases[1::2]
        '''
        labels_train[:] = labels[:len(labels)//2] #half data
        cases_train[:] = cases[:len(labels)//2]
        '''
        minmaxcases_train = applyminmax(cases_train)
        minmaxlabels_train = applyminmax(labels_train)
        
        self.setup(4, 5, 1)
        self.train(minmaxcases_train, minmaxlabels_train, 10000, 0.05, 0.1)
        
        #test part
        
        labels_test[:] = labels[::2] #odd index to get test data
        cases_test[:] = cases[::2]
        '''
        labels_test[:] = labels[len(labels)//2:] #half data
        cases_test[:] = cases[len(labels)//2:]
        '''
        x = np.array(labels_test)
        amax=x.max(axis = 0)
        amin=x.min(axis = 0)
        
        minmaxcases_test = applyminmax(cases_test)
               
        for case in minmaxcases_test:
            predict = self.predict(case)*(amax-amin)+amin
            predict_list.append(predict)
            
        compute_mse(predict_list, labels_test)
            
        plt.title('Stock price prediction')
        plt.ylabel('price')
        plt.plot(labels_test,label="true price")
        plt.plot(predict_list,label='predicted price')
        plt.legend()
        plt.savefig('NN_price.png')
        

if __name__ == '__main__':
    nn = BPNeuralNetwork()
    nn.test()
