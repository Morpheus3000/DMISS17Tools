# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:40:09 2017

@author: hagen

(Modified by Partha Das on 29-06-2017)
"""

import json
import os
import time
import pandas as pd
import re
import datetime

def cleaned_url(s):
    """ Function to clean up multiple trailing ')', '.', '*' """
    l = 0
    s = s.strip()
    for c in reversed(s):
        if c == ')' or c == '.' or c == '*' or c == ',':
            l += 1
        else:
            break
    if l > 0:
        tmp = s[:-l]
        return tmp

    else:
        return s
    

def filterURLs(inputfile, outputfile, searchfor):
    """ Function to parse through the input csv and filter only the URLs
    specified by the filter.
    @Params:
        inputfile: The relative location of the input csv
        outputfile: The relative of where the filtered output should be saved
        searchfor: The filter list to be searched for in the urls
    """

    with open(inputfile, 'r') as file:
        csvobject = pd.read_csv(file)

    urls = csvobject.body.str.contains('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', na=False)

    urlcomments = pd.DataFrame(csvobject[urls])
    newurlcomments = urlcomments.body.str.extractall("(?P<imageurl>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)")

    columns = ['index','match','imageurl','name', 'author', 'ups', 'name']

    contextdf = pd.DataFrame(columns=columns)
    indices = []
    matches = []
    dates = []
    formatteddates = []
    imageurls = []
    bodies = []
    authors = []
    subreddits = []
    scores = []


    for index, line in newurlcomments.iterrows():
        tmp = cleaned_url(line.imageurl)
        if len(re.findall(r'|'.join(searchfor), tmp)) > 0:
            newindex=index[0]
            newdate = csvobject.created_utc[newindex]
            formatteddate = datetime.datetime.fromtimestamp(int(newdate)).strftime('%Y-%m-%d %H:%M:%S')
            newbody = csvobject.body[newindex]
            newauthor = csvobject.author[newindex]
            newsubreddit = csvobject.subreddit[newindex]
            newscore= csvobject.score[newindex]
            indices.append(newindex)
            matches.append(index[1])
            dates.append(newdate)
            formatteddates.append(formatteddate)
            imageurls.append(tmp)
            bodies.append(newbody)
            authors.append(newauthor)
            subreddits.append(newsubreddit)
            scores.append(newscore)

    contextdf['index'] = indices
    contextdf['match'] = matches
    contextdf['created_unix'] = dates
    contextdf['created_time'] = formatteddates
    contextdf['imageurl'] = imageurls
    contextdf['name'] = bodies
    contextdf['author'] = authors
    contextdf['reactionscount'] = scores
    contextdf['subreddit'] = subreddits
    contextdf.to_csv(outputfile, index=False)

if __name__ == '__main__':
    starttime = time.time()
    print('code started')
    #ENTER SEARCH TERMS
    searchfor = ['.png', '.gif', '.jpg']
    inputfile = str('RC_2008-05.csv')
    outputfile = str(inputfile[:-4]) + '-imageurl.csv'
    print("\n\n\nJob parameters:\n\tInput ---> %s\n\tFilters ---> %s\n\tOutput --->%s\n\n\n" % (inputfile, '|'.join(searchfor), outputfile))
    filterURLs(inputfile, outputfile, searchfor)
    print(time.time() - starttime)
