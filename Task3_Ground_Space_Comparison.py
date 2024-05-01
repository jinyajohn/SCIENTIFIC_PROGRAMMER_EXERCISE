#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:29:10 2024

@author: jinya
"""

#------- TASK 3: COMPARING GROUND-BASED AND SPACEBORNE AEROSOL OPTICAL PROPERTIES ---#

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import glob
import os


def temp_closest(t1,t2,t_sat):   # function to calculate the minimum time difference between ground lidar and satellite
    t_start = datetime(1970, 1, 1, 00, 00, 00)+timedelta(seconds=t1[0])
    t_end = datetime(1970, 1, 1, 00, 00, 00)+timedelta(seconds=t2[0])
    diff1,diff2 = t_sat-t_start,t_sat-t_end
    time_diff1 = (abs(diff1.total_seconds()))
    time_diff2 = (abs(diff2.total_seconds()))
    time_diff = [time_diff1,time_diff2]
    return time_diff


# read the dataset

f1 = nc.Dataset('/Users/jinya/Documents/TROPOS_Germany/03-Calipso+ground_lidar/Mindelo_station_L2_5km_lon_-24.99_lat_16.88_Radius-300_km_2021_09.nc')

BSC_T = f1.groups['TOTAL_AEROSOL'].variables['beta'][:]
BSC_sat = BSC_T.data      #km-1 sr-1
lat_sat = f1.variables['Latitude'][:].data
lon_sat = f1.variables['Longitude'][:].data
altitude_sat = f1.variables['Altitude'][:].data  # in km 
Distance_sat = f1.variables['Distances'][:].data
day_sat = f1.variables['Day'][:].data
time_sat = datetime.strptime("17/9/2021 5:15:00", "%d/%m/%Y %H:%M:%S")   #considering time as 05:15:00 UTC
f1.close()

# finding the closest point by using the distance from the station to the satellite overpass (Distance in dataset)
I = np.squeeze(np.where(day_sat==17))    #corresponds to September 17
K = np.where(Distance_sat[I]==Distance_sat[I].min())
J = I[K]   # index of closest distance

# picking satellite profile corresponding to the index J 
backsc_sat = BSC_sat[J,:]

#  Section to choose the ground lidar file closest to the satellite overpass
f_polly = glob.glob('/Users/jinya/Documents/TROPOS_Germany/03-Calipso+ground_lidar/PollyXT_profiles/*.nc')
f_polly.sort()
T_diff = []
path = '/Users/jinya/Documents/TROPOS_Germany/03-Calipso+ground_lidar/PollyXT_profiles'   #path for PollyXT files 
# iterating over the loop to obtain the time difference between ground and sat files
for i in np.arange(0,len(f_polly)):
    file = os.path.basename(f_polly[i])
    filename = os.path.join(path,file)
    f2 = nc.Dataset(filename)
    time1= f2.variables['start_time'][:].data
    time2 = f2.variables['end_time'][:].data
    t_diff = temp_closest(time1,time2,time_sat)   # function returning differece of time between ground observation and satellite
    T_diff.append(t_diff)
    f2.close()
    
T_diff = np.array(T_diff)  
K_match = np.array(np.where(T_diff==T_diff.min()))  #index corresponding to the minimum time difference 
K_match = K_match[np.unravel_index(0, K_match.shape)]
file_closest = os.path.join(path,f_polly[K_match])  # file closest in time and space
f3 = nc.Dataset(file_closest)
backsc_polly = f3.variables['aerBsc_raman_532'][:].data*(10**3) # given m-1 sr-1 ; so unit conversion to km-1 sr-1
H_polly = f3.variables['height'][:].data*0.001   #converting to km
f3.close()

# comparing backscatter coefficient
# This part is remaining 
