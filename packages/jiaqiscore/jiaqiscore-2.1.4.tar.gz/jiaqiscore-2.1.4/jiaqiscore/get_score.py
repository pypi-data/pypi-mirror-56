# -*- encoding:utf-8 -*-

import pandas as pd
import numpy as np
import random
import math
import time

def get_train_csv(train_path):
    train_data = pd.read_csv(train_path)
    return train_data

def get_test_csv(test_path):
    test_data = pd.read_csv(test_path)
    return test_data

def logloss(y_true, y_pred, l):
    eps = 1e-15
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    assert (len(y_true) and len(y_true) == len(y_pred))

    p = np.clip(y_pred, eps, 1-eps)
    a = np.sum(- y_true * np.log(p))
    loss = (1 - (a / l)) * 100

    return loss

def unitest(y_true,y_pred,l):

    loss = logloss(y_true, y_pred,l)

    return loss

def get_loss_by_bendi(train_path,test_path):
    train_data = get_train_csv(train_path)
    test_data = get_test_csv(test_path)
    if train_data.shape[0] != test_data.shape[0]:
        print("The train_length and test_length is different!")
        return None
    y_true = []
    y_pred = []
    length = 0
    df_merge = pd.merge(train_data,test_data,on='NSRSBH')
    for index,row in df_merge.iterrows():
        if int(row['Result']) == 1:
            y_true.append(row['Result'])
            y_pred.append(row['Probability'])
            length = length + 1
    loss = unitest(y_true,y_pred,length)
    return loss

def get_loss_by_yunanbao(train,test):
    if train.shape[0] != test.shape[0]:
        print("The train_length and test_length is different!")
        return None
    y_true = []
    y_pred = []
    length = 0
    df_merge = pd.merge(train,test,on='NSRSBH')
    for index,row in df_merge.iterrows():
        if int(row['Result']) == 1:
            y_true.append(row['Result'])
            y_pred.append(row['Probability'])
            length = length + 1
    loss = unitest(y_true,y_pred,length)
    return loss

def getscore(train_path,test_path):
    start = time.time()
    score = get_loss_by_yunanbao(train=train_path,test=test_path)
    end = time.time() - start
    if end < 60:
        score = score*0.9 + 1
    elif end>=60 and end<120:
        score = score*0.9 + 0.7
    elif end>=120 and end<360:
        score = score*0.9 + 0.5
    elif end>=360 and end<600:
        score = score*0.9 + 0.3
    else:
        score = score*0.9 + 0.1
    return score
