#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../utils')

from get_open_close import populate_values_efficient

def kmeans_automated(start_date, end_date, k=5, max_iter=1000):
    
    all_stocks = populate_values_efficient(start_date, end_date)
    
    all_stocks_open = []
    all_stocks_close = []

    for stock in all_stocks:
        stock_sym, attribute = stock
        if attribute == 'Open':
            all_stocks_open.append(pd.DataFrame(all_stocks[stock_sym]['Open']).rename(columns={'Open': stock_sym}))
        elif attribute == 'Close':
            all_stocks_close.append(pd.DataFrame(all_stocks[stock_sym]['Close']).rename(columns={'Close': stock_sym}))

    all_stocks_open_df = pd.concat(all_stocks_open, axis=1)
    all_stocks_close_df = pd.concat(all_stocks_close, axis=1)
    
    stock_names = list(all_stocks_open_df.columns)
    
    open_values = np.array(all_stocks_open_df.T)
    close_values = np.array(all_stocks_close_df.T)
    
    daily_movements = close_values - open_values

    # create the model pipeline
    normalizer = Normalizer()
    clustering_model = KMeans(n_clusters=k, max_iter=max_iter)
    pipeline = make_pipeline(normalizer, clustering_model)
    pipeline.fit(daily_movements)
    clusters = pipeline.predict(daily_movements)
    
    # get results
    results = pd.DataFrame({
        'clusters': clusters,
        'symbols': stock_names
    }).sort_values(by=['clusters'], axis=0)
    
    return results
