
import os
import glob
import time
import pandas as pd
import re
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import linkRipper



dir_list = [str(x + 1) for x in range(6)]
parent_dir = '4chanData'

idx = 0

a = time.time()
columns = ['index', 'country_name', 'com', 'raw_com', 'name', 'sub', 'replies', 'now']
valids = ['www.youtube.com', 'youtu.be']
searchfor = ['cuck' 'globalist' 'sjw' 'tendies' 'maga' 'based' 'kek' 'pepe' 'sjw' 'globalist' 'establishment' 'elite' 'neocon' 'sanders' 'gop' 'trump' 'communist' 'tpp' 'borders' 'mccain' 'soros' 'china' 'mexico'] # Leave empty for no filtering

mainStore = pd.DataFrame(columns=columns)
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

