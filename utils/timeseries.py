#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np


"""We have used this code snippet for formatting time series from: https://youtu.be/tepxdcepTbY"""
def get_timeseries_X_y(x_train):
    n_future = 1
    n_past = 14
    x_train_final = []
    y_train_final = []

    for idx in range(n_past, len(x_train) - n_future +1):
        x_train_final.append(x_train[idx - n_past:idx, 0:x_train.shape[1]])
        y_train_final.append(x_train[idx + n_future - 1:idx + n_future, 1])
    
    return np.array(x_train_final), np.array(y_train_final)