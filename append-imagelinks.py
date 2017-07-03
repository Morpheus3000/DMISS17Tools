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
inputfile = str('csv-output/RC_2008-05.csv')

#ENTER SEARCH TERMS
searchfor = ['.png', '.gif', '.jpg']

outputname = str(inputfile[:-5]) + '-imageurl.csv'

with open(inputfile, 'r') as file:
#    for line in jsoncollection:

    csvobject = pd.read_csv(file)
    
#    stringcheck = csvobject[csvobject.body.str.contains('|'.join(searchfor), na=False)]
#    stringcheck = csvobject[csvobject.body.str.contains('|'.join(searchfor), na=False)]
#    urlpattern= r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = csvobject.body.str.contains('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', na=False)
    urlcomments = pd.DataFrame(csvobject[urls])
#    print(urlcomments)
#    urlli = stringcheck.body.str.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


    newurlcomments = urlcomments.body.str.extractall("(?P<imageurl>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)")
#    print(newurlcomments)
    indexarray = newurlcomments.index.levels[0]
    
    columns = ['name', 'author', 'ups', 'name']

    contextdf = pd.DataFrame(columns=columns)
    bodies = []
    authors = []
    subreddits = []
    scores = []
    
    
    for index, line in newurlcomments.iterrows():
        newindex=index[0]
        newbody = csvobject.body[newindex]
        newauthor = csvobject.author[newindex]
        newsubreddit = csvobject.subreddit[newindex]
        newscore= csvobject.score[newindex]
        bodies.append(newbody)
        authors.append(newauthor)
        subreddits.append(newsubreddit)
        scores.append(newscore)

    newurlcomments['name'] = bodies
    newurlcomments['author'] = authors
    newurlcomments['reactionscount'] = scores
    newurlcomments['subreddit'] = subreddits
    print(newurlcomments)


    newurlcomments.to_csv('imgtest.csv')

    
    
#    urlcomments = urlcomments.assign(imageurl = body)
#    urlcomments.to_csv(outputname)
#    print(urlcomments)
#    for row in urlcomments:
#        print(row)
#        newstring = re.search('.jpg', line.body.str).group(1)
#        print(newstring)
#        for url in line:
#            if len(url) > 1:
#                l = 0
#                for c in reversed(url):
#                    if c == '.' or c == ')' or c == '*':
#                        l += 1
#                    else:
#                        break
#                if l > 0:
#                    tmp = url[:-l]
#                    if len(re.findall(r'|'.join(searchfor), tmp)) > 0:
#                        newstring.append(tmp)
#        if len(newstring) > 1:
#            output.write(','.join(newstring)+'\n')

print(time.time() - starttime)
