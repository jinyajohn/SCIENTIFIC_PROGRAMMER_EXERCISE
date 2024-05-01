#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:23:14 2024

@author: jinya
"""


#---------- TASK 1 : FEATURE MASK VISUALISATION ----------------#

import numpy as np
import h5py
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
from datetime import datetime
from time import strftime
from datetime import timedelta
from haversine import haversine
import os



def great_circle_dist_calc(center,lat_lon):   # calculating distance between two coordinates
    d = np.array([haversine(Center,point) for point in lat_lon])
    return d

def time_calc(Time):   # calculating time since 2000-01-01 00:00:00.00
    time = [(datetime(2000, 1, 1, 00, 00, 00)+timedelta(seconds=tt)) for tt in Time]  
    return time

def find_var(index):      # function to pick data points of interest 
    Time = hfile[fkey]['time'][index]
    Height = (hfile[fkey]['height'][index])*0.001
    fmask = hfile[fkey]['featuremask'][index]
    return(Time,Height,fmask)
    
def plotmask(data):          # plotting data
    # setting colorbar ticks
    fig = plt.subplots(figsize=(8,8))
    cbar_ticks = list(range(data.values.min(),data.values.max()+1,1))
    ax = sn.heatmap(data,cmap=sn.color_palette("viridis", 14),vmin=-3.5, vmax=10.5, cbar_kws={'label': 'Feature Mask','ticks': cbar_ticks})    
    # setting x tciks
    intervalx = ((data.columns[-1]-data.columns[0]).total_seconds())/(len(data.columns))
    desired_intervalx = int(60/intervalx)
    Xticks = [ticks for ticks in list(range(0,len(data.columns),desired_intervalx))]
    Xlabels = [data.columns[j].strftime('%H:%M:%S') for j in Xticks]    
    ax.set_xticks(Xticks)
    ax.set_xticklabels(Xlabels,weight='bold',size=8)
    ax.tick_params(axis='x', labelrotation=45)   
    ax.set_xlabel('Time in UTC', weight='bold')    
    #setting y ticks
    intervaly = (data.index.max()-data.index.min())/len(data.index)
    desired_intervaly = int(abs(3/intervaly))
    Yticks = [ticks for ticks in list(range(0,len(data.index),desired_intervaly))]
    ylabels=[data.index[i] for i in Yticks]
    ax.set_yticks(Yticks)
    ax.set_ylabel('Height [km]',weight='bold')
    ax.set_yticklabels(ylabels,weight='bold') 
    ax.annotate('10: likely very thick clouds, 7-9: strong features, 5-8: weak features,'+ '\n' + '0: clear sky, -1: attenuated pixels, -3: direct surface return',xy=(0.5, 0),xytext=(0,-8))
    return ax

   

# --------reading file and accessing variables----------#
hfile = h5py.File('ECA_EXAA_ATL_FM__2A_20241231T183450Z_20230131T101420Z_39316D.h5','r')
fkey = list(hfile.keys())[1]
lat = hfile[fkey]['latitude'][:]
lon = hfile[fkey]['longitude'][:]

# Part 1: VISUALISING FEATURE MASK AROUND A RADIUS OF 500 KM ----------#
Center = (44.6,-63.6) 
P = list(zip(lat,lon))
dist = great_circle_dist_calc(Center,P)
I = np.where(dist<=500)         #radius=500 km
time1,height1,mask1 = find_var(I)    # picking data within a radius of 500 km
time = time_calc(time1)

# choosing height till 18 km corresponding to tropopause height
H = np.array([format(ht,"0.2f") for ht in height1[0,:]],dtype=float)
K = np.squeeze(np.where((H>0) & (H<=18)))
height = H[K]

# creating a dataframe
data1 = pd.DataFrame(data=mask1[:,K].T, index=height, columns=time)

f = plotmask(data1)  # calling the plotmask function to generate mask image
 
del I,mask1,time,time1,data1,height1,height,H


# Uncomment this part to plot for points around a radius of 1000 km

## --------- Part 2: VISUALISING FEATURE MASK AROUND A RADIUS OF 1000 km ----------#

Center = (44.6,-63.6) 
P = list(zip(lat,lon))
dist = great_circle_dist_calc(Center,P)      
I = np.where(dist<=1000)         #radius=1000 km
time1,height1,mask1 = find_var(I)
time = time_calc(time1)
# choosing height till 18 km corresponding to tropopause height
H = np.array([format(ht,"0.2f") for ht in height1[0,:]],dtype=float)
K = np.squeeze(np.where((H>0) & (H<=18)))
height = H[K]

data1 = pd.DataFrame(data=mask1[:,K].T, index=height, columns=time)

f = plotmask(data1)


