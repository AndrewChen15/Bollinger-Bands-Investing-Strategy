#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:50:58 2023

@author: andrewchen
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_bollinger_bands(df, window = 21, no_of_std = 1, column_name = ''):
    
    
    adf = pd.DataFrame(columns=['Observation','RollingMean','UpperBound','LowerBound', 'Standarddev'])
    
    if column_name == '':
        adf['Observation'] = df[0]
        w = df[0].rolling(window, min_periods = 1)
        adf['RollingMean'] = w.mean()
        adf['Standarddev'] = w.std()
        adf['UpperBound'] = adf['RollingMean'] + (adf['Standarddev'] * no_of_std)
        adf['LowerBound'] = adf['RollingMean'] - (adf['Standarddev'] * no_of_std)
        
        del adf['Standarddev']
        
        adf['Observation'].plot(label = 'Observation')
        adf['RollingMean'].plot(label = 'RollingMean')
        adf['UpperBound'].plot(label = 'UpperBound')
        adf['LowerBound'].plot(label = 'LowerBound')
        plt.legend()
        
        plt.xlabel('Date')
        
        plt.title('Observations with Bollinger Bands')
        
    
    else:
        adf['Observation'] = df[column_name]
        w = df[column_name].rolling(window, min_periods = 1)
        adf['RollingMean'] = w.mean()
        adf['Standarddev'] = w.std()
        adf['UpperBound'] = adf['RollingMean'] + (adf['Standarddev'] * no_of_std)
        adf['LowerBound'] = adf['RollingMean'] - (adf['Standarddev'] * no_of_std)
        
        del adf['Standarddev']
       
        adf['Observation'].plot(label = 'Observation')
        adf['RollingMean'].plot(label = 'RollingMean')
        adf['UpperBound'].plot(label = 'UpperBound')
        adf['LowerBound'].plot(label = 'LowerBound')
        plt.legend()
        
        plt.xlabel('Date')
        
        plt.title('Observations with Bollinger Bands')
       
    return adf

def create_long_short_position(df):
    
    
    adf = df[:]
    
    position = pd.Series(index = df.index, data = None)
    
    
    for i in range(len(adf)):
        
        if adf['Observation'].iloc[i-1] >= adf['UpperBound'].iloc[i-1]:
            
            position[i] = 1 ## BUY
            
        elif adf['Observation'].iloc[i-1] <= adf['LowerBound'].iloc[i-1]:
            
            position[i] = -1 ## SELL
    
              
    position = position.fillna(method = 'ffill')
    
    adf['Position'] = position
    
    plt.plot(adf['Position'], label = 'Position')
    
    plt.legend()
    
    plt.xlabel('Date')
        
    plt.title('Long/Short position')

    return adf

def calculate_long_short_returns(df, position, column_name = ''):
    
    
    adf = pd.DataFrame(columns= ['Market Return', 'Strategy Return', 'Abnormal Return'])
    
    gdf = df[:]
    
    if column_name == '':
    
        l = gdf[0] / gdf[0].shift(1) - 1
    
        adf['Market Return'] = l 
    
        s = position['Position'] * adf['Market Return']
    
        adf['Strategy Return'] = s
    
        adf['Abnormal Return'] = adf['Strategy Return'] - adf['Market Return']
        
        plt.plot(adf['Market Return'], label = 'Market Return')
        
        plt.plot(adf['Strategy Return'], label = 'Strategy Return')
        
        plt.plot(adf['Strategy Return'], label = 'Strategy Return')
        
        plt.legend()
        
        plt.xlabel('Date')
        
        plt.title('Market Return, Strategy Return and Abnormal Return')
        
    else:
         l = gdf[column_name] / gdf[column_name].shift(1) - 1
    
         adf['Market Return'] = l 
    
         s = position['Position'] * adf['Market Return']
    
         adf['Strategy Return'] = s
    
         adf['Abnormal Return'] = adf['Strategy Return'] - adf['Market Return']
         
         plt.plot(adf['Market Return'], label = 'Market Return')
        
         plt.plot(adf['Strategy Return'], label = 'Strategy Return')
        
         plt.plot(adf['Strategy Return'], label = 'Strategy Return')
        
         plt.legend()
        
         plt.xlabel('Date')
        
         plt.title('Market Return, Strategy Return and Abnormal Return')
    return adf

def plot_cumulative_returns(df):
    
    
    df[['Market Return', 'Strategy Return', 'Abnormal Return']].cumsum().plot()