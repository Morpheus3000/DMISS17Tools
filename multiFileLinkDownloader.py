
import os
import glob
import time
import pandas as pd
import re
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import linkRipper



dir_list = ['../cultural-marxism/']
parent_dir = ''

idx = 0

a = time.time()

idx = 0
for sub_dir in dir_list:
    files = glob.glob(os.path.join(parent_dir, sub_dir, '*.csv'))
    for file in files:
        idx += 1
        print("[%s] Processing file %s ..." % (idx, file), end='\r')
        b = time.time()


        linkRipper.get_URLs(file, 'imageurl')

        
        print("[%s] Processing file %s ...... Done in %0.2f seconds!" % (idx,
                                                                         file,
                                                                        (time.time()-b)))
print("Completed in %0.2f seconds" % (time.time() - a))

