#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 16:43:16 2018

@author: soominy
"""

# =============================================================================
# This module is for 
# 1) extracting decision made in the system (switched or not) by evaluating the frequent OD before and after new line
# 2) feature engineering to see if it's rush-hour traveller or not before new line
# 3) feature engineering: dummy variables for the OD stations used BEFORE new line opened
# 4) Feature engineering: the physical distance between the frequent OD's to the _closest_ station in the new line
# using the 'result' data frame from Module0_1
# =============================================================================

import pandas as pd
import numpy as np 
import geopy.distance


result=pd.read_hdf('result.hdf', 'result')
metro_info=pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/Station_lat_lng_new.csv")
tempcol = pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/header.csv")
thur_after=  pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150430.csv", header=None)
thur_after.columns=tempcol.columns


# =============================================================================
# # 1) Decision extraction: find out if they switched or not
# =============================================================================
# Result: Switch column in 'result' dataframe
# =============================================================================
# new line is 3, and one station among line 3 is station ID 105.
new_line_stations = list(set(thur_after.loc[thur_after['StationId']==105, 'Line_Id']))
#the result says that the line ID is 7 in data, for the LINE 3 in Nanjing
#extract the stations that have line Id as 7 in data.
new_line_stations = list(set(thur_after.loc[thur_after['Line_Id']==new_line_stations[0], 'StationId']))
new_line_stations = metro_info.loc[metro_info["STATIONID"].isin(new_line_stations),:]
#consider the stations that have only ONE line through
#ex) delete Taifenglu
disregard_stations = [73, 26, 14]
new_line_stations =new_line_stations.loc[ np.logical_not(new_line_stations['STATIONID'].isin(disregard_stations)),: ]
new_line_stations =new_line_stations.reset_index()
metro_info["NewLine"]=0
metro_info.loc[metro_info["STATIONID"].isin(new_line_stations["STATIONID"]),"NewLine"]=1

result['Switch']=0
result.loc[ (result['Freq_O1_A'].isin(new_line_stations['STATIONID'])) |
        (result['Freq_O2_A'].isin(new_line_stations['STATIONID'])) |
        (result['Freq_D1_A'].isin(new_line_stations['STATIONID'])) |
        (result['Freq_D2_A'].isin(new_line_stations['STATIONID'])) ,"Switch"] = 1


#result.to_hdf('result.hdf','result')
# =============================================================================



# =============================================================================
# # 2) Feature Engineering: dummy variable for rush-hour traveller or not BEFORE NEW LINE
# =============================================================================
# BASED ON DEPARTURE TIME
# Result: RushHour_AM, RushHour_PM, RushHour_Both columns in 'result' dataframe
# =============================================================================
result['RushHour_AM']=0
result['RushHour_PM']=0
result['RushHour_Both']=0 #they travel at rush hour both in morning and after peaks
RushHour_AM=[7,8,9]
RushHour_PM=[17,18,19]
result.loc[ ((result['Freq_DT1_B'].isin(RushHour_AM)) |
        (result['Freq_DT2_B'].isin(RushHour_AM)))  ,"RushHour_AM"] = 1
result.loc[ ((result['Freq_DT1_B'].isin(RushHour_PM)) |
        (result['Freq_DT2_B'].isin(RushHour_PM)))  ,"RushHour_PM"] = 1
result.loc[ ((result['Freq_DT1_B'].isin(RushHour_PM)) &
        (result['Freq_DT2_B'].isin(RushHour_PM)))  ,"RushHour_Both"] = 1


#result.to_hdf('result.hdf','result')
# =============================================================================



        
        
        
        




 
# =============================================================================
# # 3) Feature engineering: dummy variables for the OD stations used BEFORE new line opened
# =============================================================================
# Result: Freq_O1_xx, Freq_O2_xx, Freq_D1_xx, Freq_D2_xx, Freq_Any_xx columns, where xx=station ID numbers
# example) O2_3 column is the dummy variable for using station 3 as the second most frequent origin station,
#           its value only in [1,0]
# example) Any_5 column is the dummy variable for using station 5 as any of the two frequent O's or two frequent D's
#           its value possible in [2,1,0], as 2 means the staiton 5 appears appear both in frequent O and D.
# =============================================================================

dummy1= pd.get_dummies(result["Freq_O1_B"]) #data frame for using each station for the most most frequent O
dummy2= pd.get_dummies(result["Freq_O2_B"]) #data frame for using each station for the second most frequent O
dummy3= pd.get_dummies(result["Freq_D1_B"]) #data frame for using each station for the most frequent D
dummy4= pd.get_dummies(result["Freq_D2_B"]) #data frame for using each station for the second most frequent D
dummy_total=dummy1+dummy2+dummy3+dummy4 #data frame for using each station for any of two frequent O/Dach station for the most frequent O

newcol =["Freq_O1_" + str(s) for s in list(dummy1.columns.values)]
oldcol = dummy1.columns
dummy1.rename(columns=dict(zip(oldcol,newcol)), inplace=True)

newcol =["Freq_O2_" + str(s) for s in list(dummy2.columns.values)]
oldcol = dummy2.columns
dummy2.rename(columns=dict(zip(oldcol,newcol)), inplace=True)

newcol =["Freq_D1_" + str(s) for s in list(dummy3.columns.values)]
oldcol = dummy3.columns
dummy3.rename(columns=dict(zip(oldcol,newcol)), inplace=True)

newcol =["Freq_D2_" + str(s) for s in list(dummy4.columns.values)]
oldcol = dummy4.columns
dummy4.rename(columns=dict(zip(oldcol,newcol)), inplace=True)

newcol =["Freq_Any_" + str(s) for s in list(dummy_total.columns.values)]
oldcol = dummy_total.columns
dummy_total.rename(columns=dict(zip(oldcol,newcol)), inplace=True)


result = pd.concat([result, dummy1, dummy2, dummy3, dummy4, dummy_total], axis=1)
# =============================================================================








# =============================================================================
# # 4) Feature engineering: the physical distance between the frequent OD's to the _closest_ station in the new line
# =============================================================================
# # Result: Columns called MinDistToNew_O1_B,MinDistToNew_O2_B,MinDistToNew_D1_B,MinDistToNew_D2_B in "result"
# =============================================================================

#Compute the distance between each station frequently used BEFORE new line opened to the closest new station on line 3
metro_info["MinDistToNewSt"]=0
for i in range(0,len(metro_info["STATIONID"])):
    min_dist = 100000000000000000000000
    for j in range(0,len(new_line_stations["STATIONID"])): 
        dist = geopy.distance.vincenty( (metro_info.loc[i,"lat"],metro_info.loc[i,"lng"]),  
                                       (new_line_stations.loc[j,"lat"],new_line_stations.loc[j,"lng"]) ).km
        min_dist=min(min_dist,dist)
    metro_info.loc[i,"MinDistToNewSt"]=min_dist

#Allocate the minimum distance to a new station for each frequent ODs
temp1 = metro_info[["STATIONID","MinDistToNewSt"]] 
#temp2 = result[["Freq_O1", "Freq_O2","Freq_D1","Freq_D2"]]
save=result

temp1=temp1.rename(columns={'STATIONID':'Freq_O1_B'})
result=pd.merge(result,temp1, on="Freq_O1_B",how="left")
result=result.rename(columns={"MinDistToNewSt":"MinDistToNew_O1_B"})

temp1=temp1.rename(columns={'Freq_O1_B':'Freq_O2_B'})
result=pd.merge(result,temp1, on="Freq_O2_B", how="left")
result=result.rename(columns={"MinDistToNewSt":"MinDistToNew_O2_B"})

temp1=temp1.rename(columns={'Freq_O2_B':'Freq_D1_B'})
result=pd.merge(result,temp1, on="Freq_D1_B", how="left")
result=result.rename(columns={"MinDistToNewSt":"MinDistToNew_D1_B"})

temp1=temp1.rename(columns={'Freq_D1_B':'Freq_D2_B'})
result=pd.merge(result,temp1, on="Freq_D2_B", how="left")
result=result.rename(columns={"MinDistToNewSt":"MinDistToNew_D2_B"})
 
#result.to_hdf('result.hdf','result')
# =============================================================================
  
