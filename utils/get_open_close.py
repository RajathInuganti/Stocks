#!/usr/bin/env python
# coding: utf-8


import pandas as pd

symbols = pd.read_csv('../dataset/symbols_valid_meta.csv')
stock_paths = {}
stock_dfs = {}


symbols_list = list(symbols['Symbol'])


for symbol in symbols_list:
    if symbol not in stock_paths:
        stock_paths[symbol] = f'../dataset/stocks/{symbol}.csv'
        
        
for symbol, stock_path in stock_paths.items():
    if symbol not in stock_dfs:
        try:
            stock_dfs[symbol] = pd.read_csv(stock_path)
        except:
            continue        

# clean data

# turn all date columns to datetime
for stock_name, stock_df in stock_dfs.items():
    stock_df['Date'] = pd.to_datetime(stock_df["Date"])
    

# remove rows with NA values
for stock_name, stock_df in stock_dfs.items():
    stock_df.dropna(how='any', inplace=True)


# helper functions


def get_rows_within_date_range(df, start_date, end_date):
    return df.loc[((df['Date'] >= start_date) & (df['Date'] <= end_date))]


def get_start_and_end_date_df(df):
    start_date = df['Date'].iloc[0]
    end_date = df['Date'].iloc[-1]
    return (start_date, end_date)


def not_compatible(df, start_date, end_date):
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    df_start, df_end = get_start_and_end_date_df(df)
    if start_date < df_start or end_date > df_end:
        return True
    else:
        return False



def populate_values_efficient(start_date, end_date):

    # CAT is the stock with the most rows, so it encompasses all date ranges
    df = get_rows_within_date_range(stock_dfs['CAT'], start_date, end_date)
    
    open_close_stocks = pd.DataFrame(columns=['Date'])
    
    open_close_stocks['Date'] = df['Date']
    benchmark = len(df)
    
    to_merge = []

    index = list(df['Date'])

    for stock_name, stock_df in stock_dfs.items():
        
        company_cols = pd.DataFrame(get_rows_within_date_range(stock_df, start_date, end_date))[['Open', 'Close']]
    
        # filter out non compatible stocks
        if not_compatible(stock_df, start_date, end_date):
            continue
            
        if len(company_cols) < len(index):
            continue

        open_col = company_cols['Open']
        close_col = company_cols['Close']

        if len(company_cols) == benchmark:
            open_col.index = index
            close_col.index = index

            arrays = [
                [stock_name, stock_name],
                ['Open', 'Close'],
            ]

            tuples = list(zip(*arrays))
            company = pd.DataFrame(zip(open_col, close_col), columns=pd.MultiIndex.from_tuples(tuples), index=index)

            to_merge.append(company.reset_index(drop=True))
  
    open_close_stocks = pd.concat(to_merge, axis=1)

    return open_close_stocks
