# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:37:25 2017

@author: hagen
"""

import json
import os
import time
import pandas as pd
import re

starttime = time.time()
print('code started')

csvobject = []
file = str('RC_2008-05.csv')

with open(file, 'r') as file:
#    for line in jsoncollection:

    csvobject = pd.read_csv(file)
#    DO SOMETHING WITH DATAFRAME



print(time.time() - starttime)
