# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 18:37:27 2020

@author: mat_c
"""

from selenium import webdriver
import time
import re
import pandas as pd
df = pd.read_excel('data.xlsx')
sLength = len(df['Restaurant'])

df['Duped'] = pd.Series(df.duplicated('Restaurant'), index=df.index)



# df = df.drop_duplicates(subset=['Restaurant'])  