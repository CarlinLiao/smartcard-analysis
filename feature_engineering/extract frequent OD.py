"""
Created on Fri Apr 13 13:53:22 2018

@author: soominy, CarlinLiao
"""
import pandas as pd
import numpy as np 

tue_before =  pd.read_csv("../nanjing-data/20150331.csv", header=None)
wed_before = pd.read_csv("../nanjing-data/20150401.csv", header=None)
thur_before = pd.read_csv("../nanjing-data/20150402.csv", header=None)

tue_after =  pd.read_csv("../nanjing-data/20150428.csv", header=None)
wed_after=  pd.read_csv("../nanjing-data/20150429.csv", header=None)
thur_after=  pd.read_csv("../nanjing-data/20150430.csv", header=None)

tempcol = pd.read_csv("../nanjing-data/header.csv")
# attach the header
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


# Find out the top two origins and two destinations per ID
result = pd.DataFrame(unique_id)
result.columns = ["Card_Id"]
result["Freq_O1"]=0
result["Freq_O2"]=0
result["Freq_D1"]=0
result["Freq_D2"]=0

 

f1=result.columns.get_loc("Freq_O1")
f2=result.columns.get_loc("Freq_O2")
f3=result.columns.get_loc("Freq_D1")
f4=result.columns.get_loc("Freq_D2")
 

for k in range(0,len(result["Card_Id"])):
#for k in range(15900,len(result["Card_Id"])):

    id=result["Card_Id"][k]
    temp_before1 = tue_before[tue_before['Card_Id']==id]
    temp_before2 = wed_before[wed_before['Card_Id']==id]
    temp_before3 = thur_before[thur_before['Card_Id']==id]
    temp = temp_before1.append(temp_before2, ignore_index=True)
    temp = temp.append(temp_before3, ignore_index=True)
    
    ### some might have only 1 frequent O's or D's
    freq_o = temp[temp['Entry_Or_Exit']==1]['StationId'].value_counts().head(2)
    freq_o = list(freq_o.reset_index()["index"])
    freq_d = temp[temp['Entry_Or_Exit']==2]['StationId'].value_counts().head(2)
    freq_d = list(freq_d.reset_index()["index"])
    
    if ((len(freq_o)<2) or (len(freq_d)<2)):
        result.loc[  result["Card_Id"]==id,"Card_Id"]=np.nan
    elif ((len(freq_o)>1) & (len(freq_d)>1)):
        #result.loc[result["Card_Id"]==id,"Freq_O1"]=freq_o[0]
        #result.loc[result["Card_Id"]==id,"Freq_O2"]=freq_o[1] 
        #result.loc[result["Card_Id"]==id,"Freq_D1"]=freq_d[0] 
        #result.loc[result["Card_Id"]==id,"Freq_D2"]=freq_d[1]  
        result.iloc[k,f1]=freq_o[0]
        result.iloc[k,f2]=freq_o[1]
        result.iloc[k,f3]=freq_d[0]
        result.iloc[k,f4]=freq_d[1]
        
        # print k # comment out to hopefully speed up script
        
    else:
        print "Error in ", k

result.to_hdf('result.hdf','result')

    
     