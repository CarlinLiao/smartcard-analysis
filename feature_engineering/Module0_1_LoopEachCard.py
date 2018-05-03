#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 13:53:22 2018

@author: soominy
"""
import pandas as pd
import numpy as np 
import sys

# =============================================================================
# This module is for 
# 1) extracting the top two most frequently used OD's before and after new line
# 2) extracting the top two most frequent departure/arrival times before and after new line
# by using Tuesday to Thursday data before and after new line
# Dates used for data before new line: 2015/3/3-5
# Dates used for data after new line: 2015/4/28-30
# =============================================================================
#New line was opened on April 1st of 2015
tue_before =  pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150303.csv", header=None)
wed_before = pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150304.csv", header=None)
thur_before = pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150305.csv", header=None)

tue_after =  pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150428.csv", header=None)
wed_after=  pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150429.csv", header=None)
thur_after=  pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/20150430.csv", header=None)

tempcol = pd.read_csv("~/Dropbox/Berkeley/2018SPRING/CE264/MY PROJECT/header.csv")
# attachthe header
tue_before.columns=tempcol.columns
wed_before.columns=tempcol.columns
thur_before.columns=tempcol.columns
tue_after.columns=tempcol.columns
wed_after.columns=tempcol.columns
thur_after.columns=tempcol.columns

# assumption: only consider the card ID's that appear both Tuesdays, before and after  
# Note this depends only on Tuesday, not wed/thur...
unique_id = list(set(tue_before['Card_Id']).intersection(tue_after['Card_Id']))

tue_before = tue_before[tue_before['Card_Id'].isin(unique_id)]
wed_before = wed_before[wed_before['Card_Id'].isin(unique_id)] 
thur_before = thur_before[thur_before['Card_Id'].isin(unique_id)]

tue_after = tue_after[tue_after['Card_Id'].isin(unique_id)]
wed_after = wed_after[wed_after['Card_Id'].isin(unique_id)]
thur_after = thur_after[thur_after['Card_Id'].isin(unique_id)]


# Find out the top two frequent origins and two destinations per ID
# Find out the top two frequent departure/arrival times per ID, before and after new line
result = pd.DataFrame(unique_id)
result.columns = ["Card_Id"]
result["Freq_O1_B"]=0
result["Freq_O2_B"]=0
result["Freq_D1_B"]=0
result["Freq_D2_B"]=0
result["Freq_O1_A"]=0
result["Freq_O2_A"]=0
result["Freq_D1_A"]=0
result["Freq_D2_A"]=0

result["Freq_DT1_B"]=0
result["Freq_DT2_B"]=0
result["Freq_AT1_B"]=0
result["Freq_AT2_B"]=0
result["Freq_DT1_A"]=0
result["Freq_DT2_A"]=0
result["Freq_AT1_A"]=0
result["Freq_AT2_A"]=0


f1=result.columns.get_loc("Freq_O1_B")
f2=result.columns.get_loc("Freq_O2_B")
f3=result.columns.get_loc("Freq_D1_B")
f4=result.columns.get_loc("Freq_D2_B")

f5=result.columns.get_loc("Freq_O1_A")
f6=result.columns.get_loc("Freq_O2_A")
f7=result.columns.get_loc("Freq_D1_A")
f8=result.columns.get_loc("Freq_D2_A")

t1=result.columns.get_loc("Freq_DT1_B")
t2=result.columns.get_loc("Freq_DT2_B")
t3=result.columns.get_loc("Freq_AT1_B")
t4=result.columns.get_loc("Freq_AT2_B")
t5=result.columns.get_loc("Freq_DT1_A")
t6=result.columns.get_loc("Freq_DT2_A")
t7=result.columns.get_loc("Freq_AT1_A")
t8=result.columns.get_loc("Freq_AT2_A")

for k in range(0,len(result["Card_Id"])):

    id=result["Card_Id"][k]
    temp_before1 = tue_before[tue_before['Card_Id']==id]
    temp_before2 = wed_before[wed_before['Card_Id']==id]
    temp_before3 = thur_before[thur_before['Card_Id']==id]
    temp_b = temp_before1.append(temp_before2, ignore_index=True)
    temp_b = temp_b.append(temp_before3, ignore_index=True)
    
    temp_after1 = tue_after[tue_after['Card_Id']==id]
    temp_after2 = wed_after[wed_after['Card_Id']==id]
    temp_after3 = thur_after[thur_after['Card_Id']==id]
    temp_a = temp_after1.append(temp_after2, ignore_index=True)
    temp_a = temp_a.append(temp_after3, ignore_index=True)
    
    # =============================================================================
    # 1) extracting the top two most frequently used OD's before and after new line    
    # =============================================================================

    ### top most frequent OD's time before new line
    ### some might have only 1 frequent O's or D's
    freq_o_b = temp_b[temp_b['Entry_Or_Exit']==1]['StationId'].value_counts().head(2)
    freq_o_b = list(freq_o_b.reset_index()["index"])
    freq_d_b = temp_b[temp_b['Entry_Or_Exit']==2]['StationId'].value_counts().head(2)
    freq_d_b = list(freq_d_b.reset_index()["index"])
    ### top most frequent OD's time AFTER new line
    freq_o_a = temp_a[temp_a['Entry_Or_Exit']==1]['StationId'].value_counts().head(2)
    freq_o_a = list(freq_o_a.reset_index()["index"])
    freq_d_a = temp_a[temp_a['Entry_Or_Exit']==2]['StationId'].value_counts().head(2)
    freq_d_a = list(freq_d_a.reset_index()["index"])
    
    # =============================================================================
    # 2) extracting the top two most frequent departure/arrival times before and after new line
    # =============================================================================
    ### top most frequent departure/arrival time before new line, in order of increasing time
    #before new line, departure (=entry to station)
    temp_hour = pd.Series([x[11:13] for x in temp_b.loc[temp_b['Entry_Or_Exit']==1, 'Time']])
    temp_hour = temp_hour.value_counts().head(2)
    freq_dt_b = map(int,list(temp_hour.reset_index()["index"]))
    freq_dt_b.sort()
    #before new line, arrival (=exit from station)
    temp_hour = pd.Series([x[11:13] for x in temp_b.loc[temp_b['Entry_Or_Exit']==2, 'Time']])
    temp_hour = temp_hour.value_counts().head(2)
    freq_at_b = map(int,list(temp_hour.reset_index()["index"]))
    freq_at_b.sort()
    #after new line, departure (=entry to station)
    temp_hour = pd.Series([x[11:13] for x in temp_a.loc[temp_a['Entry_Or_Exit']==1, 'Time']])
    temp_hour = temp_hour.value_counts().head(2)
    freq_dt_a = map(int,list(temp_hour.reset_index()["index"]))
    freq_dt_a.sort()
    #after new line, arrival (=exit from station)
    temp_hour = pd.Series([x[11:13] for x in temp_a.loc[temp_a['Entry_Or_Exit']==2, 'Time']])
    temp_hour = temp_hour.value_counts().head(2)
    freq_at_a = map(int,list(temp_hour.reset_index()["index"]))
    freq_at_a.sort()
    
    
    if ((len(freq_o_b)<2) or (len(freq_d_b)<2) or (len(freq_o_a)<2) or (len(freq_d_a)<2) or
        (len(freq_dt_b)<2) or (len(freq_at_b)<2) or (len(freq_dt_a)<2) or (len(freq_at_a)<2)):
        result.loc[result["Card_Id"]==id,"Card_Id"]=np.nan
    elif ((len(freq_o_b)==2) & (len(freq_d_b)==2) & (len(freq_o_a)==2) & (len(freq_d_a)==2) or
          (len(freq_dt_b)==2) or (len(freq_at_b)==2) or (len(freq_dt_a)==2) or (len(freq_at_a)==2)): 
 
#         result.iloc[k,f1]=freq_o_b[0]
#         result.iloc[k,f2]=freq_o_b[1]
#         result.iloc[k,f3]=freq_d_b[0]
#         result.iloc[k,f4]=freq_d_b[1]
#         result.iloc[k,f5]=freq_o_a[0]
#         result.iloc[k,f6]=freq_o_a[1]
#         result.iloc[k,f7]=freq_d_a[0]
#         result.iloc[k,f8]=freq_d_a[1]
#         
#         result.iloc[k,t1]=freq_dt_b[0]
#         result.iloc[k,t2]=freq_dt_b[1]
#         result.iloc[k,t3]=freq_at_b[0]
#         result.iloc[k,t4]=freq_at_b[1]
#         
#         result.iloc[k,t5]=freq_dt_a[0]
#         result.iloc[k,t6]=freq_dt_a[1]
#         result.iloc[k,t7]=freq_at_a[0]
#         result.iloc[k,t8]=freq_at_a[1]
 
        tempdata= freq_o_b + freq_d_b + freq_o_a + freq_d_a+freq_dt_b+freq_at_b+freq_dt_a+freq_at_a
        result.iloc[k,range(f1,(t8+1))] = tempdata
                   
         
    else:
        print "Error in ", k
    sys.stdout.write(str(k)+'\n'); sys.stdout.flush();

#Consider only those that have more than 1 frequent O's and D's
result=result[ ~np.isnan(result["Card_Id"]) ] 
result=result.reset_index()
#result.to_hdf('result.hdf','result')
#save=result