# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:40:09 2017

@author: hagen

(Edits by Partha Das. 27-06-2017)
"""

import json
import os
import time
import pandas as pd
import re

starttime = time.time()
print('code started')

csvobject = []
testfile = str('RC_sub-TheRedPill-10upvotes-05-2015-05-201-images.csv')

#ENTER SEARCH TERMS AS PATTERNS
imgurlregex = r'(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?'
searchfor = ['.png', '.gif', '.jpg']

outputname = 'csv-output/' + str(testfile[:-5]) + '-images.csv'
       
#with open(testfile, encoding="utf8") as file:
output = open("urls.csv", "w")
with open(testfile, 'r') as file:
#    for line in jsoncollection:

    csvobject = pd.read_csv(file)
    
#    stringcheck = csvobject[csvobject.body.str.contains('|'.join(searchfor), na=False)]
    stringcheck = csvobject[csvobject.body.str.contains('|'.join(searchfor), na=False)]
#    urls = stringcheck[stringcheck.body.str.contains('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')]
    urlli = stringcheck.body.str.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    for line in urlli:
        newstring = []
        for url in line:
            if len(url) > 1:
                l = 0
                for c in reversed(url):
                    if c == '.' or c == ')' or c == '*':
                        l += 1
                    else:
                        break
                if l > 0:
                    tmp = url[:-l]
                    if len(re.findall(r'|'.join(searchfor), tmp)) > 0:
                        newstring.append(tmp)
        if len(newstring) > 1:
            output.write(','.join(newstring)+'\n')
    output.close()
print(time.time() - starttime)
