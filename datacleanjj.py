# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 18:37:27 2020

@author: mat_c
"""
from datetime import date
today = date.today()
import pandas as pd
df = pd.read_excel(str(today) +'.xlsx')
df_old = pd.read_excel('2021-04-01.xlsx')
"converting to int for min-price"
if type(df['minprice'][0]) == str:
    df['minprice'] = df['minprice'].apply(lambda x: str(x.split(',')[0]))
    df['minprice'] = df['minprice'].astype(int)
    
#duplicates see if multiple listing in different categories has advantage over non-multiple    
df['duped'] = df['Restaurant'].duplicated(keep=False)
df['duped'] = df['duped'].apply(lambda x: 1 if x == True else 0 )

#number of duplicates if more duplicates results in better results?
df['Count'] = 1
df['Count'] = df.groupby(['Restaurant']).Restaurant.transform('count')

#checking for new restaurants from 5 months ago
df_old = df_old.drop_duplicates(subset=['Restaurant'], keep='first')
df_diff = pd.concat([df,df_old]).drop_duplicates(subset=['Restaurant'],keep=False)

df['new'] = df.Restaurant.isin(df_diff.Restaurant)
df['new'] = df['new'].apply(lambda x: 1 if x == True else 0 )

df.to_excel(r'data' + str(today) + '.xlsx', index=False, header=True)