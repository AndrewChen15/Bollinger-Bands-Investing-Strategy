#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:52:30 2023

@author: andrewchen
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_mean(df, dfa, column_name = ''):
    
    adf = pd.DataFrame(columns=['Observation','High','Low','Close','Percentage'])
    
    if column_name == '':
        adf['Observation'] = df[0]
        
        adf['High'] = df['High']
        
        adf['Low'] = df['Low']
        
        adf['Close'] = df['Close']
        
        adf['Percentage'] = (adf['High'] - adf['Close'])/(adf['High'] - adf['Low']) 
        
        p = dfa[['Date','Adj Close']]
        
        p = p.rename(columns = {'Adj Close': 'Interested'})
        
        adf = adf.join(p.set_index('Date'), on = 'Date')
        
        adf['Observation'].plot(label = 'Observation')
        
        adf['High'].plot(label = 'High')
        
        adf['Low'].plot(label = 'Low')
        
        adf['Close'].plot(label = 'Close')
        
        plt.legend()
        
        plt.xlabel('Date')
        
        plt.title('Observations with Close, High and Low prices')
        
        
        
    
    else:
        adf['Observation'] = df[column_name]
        
        adf['High'] = df['High']
        
        adf['Low'] = df['Low']
        
        adf['Close'] = df['Close']
        
        adf['Percentage'] = (adf['High'] - adf['Close'])/(adf['High'] - adf['Low']) 
        
        p = dfa[['Date', column_name]]
        
        p = p.rename(columns = {column_name : 'Interested'})
        
        adf = adf.join(p.set_index('Date'), on = 'Date')
        
        adf['Observation'].plot(label = 'Observation')
        
        adf['High'].plot(label = 'High')
        
        adf['Low'].plot(label = 'Low')
        
        adf['Close'].plot(label = 'Close')
        
        plt.legend()
        
        plt.xlabel('Date')
        
        plt.title('Observations with Close, High and Low prices')
        
        
    return adf

def create_long_short_position(df,dfa):
    
    adf = df[:]
    
    pdf = dfa[:]
    
    position = pd.Series(index = df.index, data = None)
    
    
    for i in range(len(adf)):
        
        if adf['Percentage'].iloc[i-1] <= 0.2:
            
            position[i] = 1 ## BUY
            
        elif adf['Percentage'].iloc[i-1] >= 0.8:
            
            position[i] = -1 ## SELL
    
              
    position = position.fillna(method = 'ffill')
    
    adf['Position'] = position
    
    l = pdf['Adj Close'] / pdf['Adj Close'].shift(1) - 1
    
    adf['Market Return'] = l 
    
    s = adf['Position'] * adf['Market Return']
    
    adf['Return'] = s
    
    del adf['Market Return']
    
    position.plot(label = 'Position')
    
    plt.legend()
    
    return adf


def create_return(df,position,commision = 0):
    
    adf = pd.DataFrame(columns= ['Market Return', 'Strategy Return', 'Abnormal Return'])
    
    
    gdf = df[:]
    
    if commision == 0:
        
        l = gdf['Adj Close'] / gdf['Adj Close'].shift(1) - 1
    
        adf['Market Return'] = l 
    
        adf['Strategy Return'] = position['Return']
    
        adf['Abnormal Return'] = adf['Strategy Return'] - adf['Market Return']
        
        adf['Market Return'].plot(label = 'Market Return')
        
        adf['Strategy Return'].plot(label = 'Strategy Return')
        
        adf['Abnormal Return'].plot(label = 'Abnormal Return')
        
        plt.legend()
        
        
    
    else:
        
        l = gdf['Adj Close'] / gdf['Adj Close'].shift(1) - 1
    
        adf['Market Return'] = l 
    
        s = position['Position'] * adf['Market Return']
    
        adf['Strategy Return'] = s * (1-commision)
    
        adf['Abnormal Return'] = adf['Strategy Return'] - adf['Market Return']
        
        adf['Market Return'].plot(label = 'Market Return')
        
        adf['Strategy Return'].plot(label = 'Strategy Return')
        
        adf['Abnormal Return'].plot(label = 'Abnormal Return')
        
        plt.legend()
        
    return adf

def plot_cumulative_returns(df):
   
    
    df[['Market Return', 'Strategy Return', 'Abnormal Return']].cumsum().plot()
    
def descriptive(df):
   
    
    adf = df[:]
    
    gdf = pd.DataFrame(columns= ['Market Return', 'Strategy Return','Abnormal Return'], index = ['Mean', 'Std', 'Cumulative'])
    
    gdf.iloc[0] = {'Market Return': adf['Market Return'].mean(), 'Strategy Return': adf['Strategy Return'].mean()}
    
    gdf.iloc[1] = {'Market Return': adf['Market Return'].std(), 'Strategy Return': adf['Strategy Return'].std()}
    
    gdf.iloc[2] = {'Abnormal Return': adf['Abnormal Return'].sum()}
    
    return gdf