import time
import pandas as pd
import urldownload

with open('../../CleanedYoutube.csv', 'r') as f:
    df = pd.read_csv(f)

vidPattern = 'http://img.youtube.com/vi/%s/0.jpg'
Folder = '../../YoutubeThumbs'

idx = 0
a = time.time()
for ids in df['videoId']:
    idx += 1
    print("[%d] Downloading %s ..." % (idx, vidPattern % ids), end='\r')
    ret = urldownload.downloadImages(vidPattern % ids, '%s\%s.jpg' % (Folder, ids))
    print("[%d] Downloaded %s ...... %r" %(idx, vidPattern % ids, ret))
print("Done in %0.2f minutes" % ((time.time() - a) / 60))
