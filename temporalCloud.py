"""Helper function to download an image given an url and the save location.
Returns an error if fails to download. 1 otherwise."""

import urllib.request
import os

__author__ = "partha das"
__version__ = "1.0.0"

def unescape(s, remove=False):
    if not remove:
        lessThan = '<'
        greatThan = '>'
        ander = '&'
    else:
        lessThan = ''
        greatThan = ''
        ander = ''
    s = s.replace('&lt;', lessThan)
    s = s.replace('&gt;', greatThan)
    s = s.replace('&amp;', ander)
    return s

def getTemporalCloud(folder):

    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            tmpName = filename+'tmp.txt'
            df = pd.read_csv(filename)
            processed = []
            for line in df['body']:
                processed.append(unescape(line, remove=True))
            filer = open(tmpName, 'w')
            filer.writelines(processed)
            filer.close()

            # Make animation??
            wordClouder = WordCloud().generate(text)




