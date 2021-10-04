# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 18:37:27 2020

@author: mat_c
"""
from datetime import date, timedelta
today = date.today()
fourdays = date.today() - timedelta(days=6)
import pandas as pd
df = pd.read_excel(str(today) +'.xlsx')
df_old = pd.read_excel('2021-04-01.xlsx')
df_4 = pd.read_excel(str(fourdays)+ '.xlsx')
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
df_diff4 = pd.concat([df,df_4]).drop_duplicates(subset=['Restaurant'],keep=False)


df['new'] = df.Restaurant.isin(df_diff.Restaurant)
df['new'] = df['new'].apply(lambda x: 1 if x == True else 0 )

#check for 4 day new register

df['new4'] = df.Restaurant.isin(df_diff4.Restaurant)
df['new4'] = df['new4'].apply(lambda x: 1 if x == True else 0)

foodlist = ["치킨", "피자양식", "중식", "한식", "일식돈까스", "족발보쌈", "야식", "분식", "카페디저트", "편의점","프랜차이즈"]
df['type'] = df['type'].apply(lambda x: foodlist.index(x))


df.to_excel(r'data' + str(today) + '.xlsx', index=False, header=True)