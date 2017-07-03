import os
import time
import re
import pandas as pd
from bs4 import BeautifulSoup

# TODOs:
#*   1) update to handle the closing }s. Fixed in the above cell
#*   2) remove the trailing commas from the elements
#*   3) clean up the html tags from the comment.
#      while cleaning the tags check what happens to the http link: More efficient to do it through pandas. Doing it while
#      creating the dataframe would need a conditional check for every read, which will slow down the process.
#      Cleans it before writing it to the csv
#*   4) add checkpointing based on the number of the record. Keep a variable. I think 500k would be a good place for the split
#      for the sample data, try with 50k to check the algorithm.
#*   5) remove the index from the pandas frame: use "index=False" when exporting to csv (or anything else)
#   6) email based notification system (Maybe. Would be fun to have. Maybe write a library)
#*   7) Check the record differences between the above 2 cells. Use another tmp file to see what is being missed.:
#      Seems only difference is the RECORD ENDED statement, which is as expected in the code. But doesn't explain the difference
#      of 1mb of filesize. Random sampling shows nothing is missing. Maybe can run a line by line check later. For now, given the
#      density of data, a few missing data points shouldn't matter. But for the library plan would be important to look into.
#*   8) Remove the quotes from the string. Breaks regex.
#   9) Drop rows with one/two/three word comments. They aren't informative.


def cleanHTMLText(html):
    soup = BeautifulSoup(html, "lxml")
    cleaned = soup.get_text()
    txt = cleaned.replace('>', '')
    txt = re.sub(r'([a-zA-Z])([:.,!?])', r'\1\2 ', txt)
    txt = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', txt)
    txt = re.sub(r'([a-z])([A-Z])', r'\1 \2', txt)
    txt = re.sub(r"^\d+\s|\s\d+\s|\s\d+$", "", txt)
    return txt

print(cleanHTMLText("test"))

columns = ["no", "resto", "now", "name", "id", "capcode", "country_name",
           "sub", "com", "replies", "capcode_replies", "last_modified", "tag",
           "semantic_url", "raw_com"]
df = pd.DataFrame(columns=columns)

checkpoint = 50000
# output_dir = '4chanSplits'
output_filename = '4chanSplits'
fileTellfilename = 'filePos.txt'
seekPoint = 2
lines = 19971930

fileTell = open(fileTellfilename, 'w')

file = open('4chan.posts.json', 'r')
file.seek(seekPoint)

started = False
tmpFrame = []

keyDict = {}
ind = 0
for name in columns:
    keyDict[name] = ind
    ind += 1

ind = 0
overall_record = 0
print("Processing file.")

splitNumber = 1
# filename = os.path.join(output_dir, output_filename + "." + str(splitNumber) + '.csv')
# output_pointer = open(filename, 'w')

endCount = 0
a = time.time()
b = time.time()
splitCounter = 0


for i in range(lines):
    line = file.readline()
    # the now attribute splits further because of the time syntax
    splits = line.strip().split(":")
    splits = [x.strip() for x in splits]
    if not line:
        break
    if len(splits) > 1 and started is False:
        if splits[1] == '{':
            tmpFrame = ["N/A" for x in columns]
            endCount = 0
            started = True
    elif len(splits) > 1 and started:
        xtractedKey = splits[0].strip('"')
        if xtractedKey in keyDict:
            tmpFilter = ':'.join(splits[1:]).replace('"', '')
            if len(tmpFilter) > 0:
                if tmpFilter[-1] == ',':
                    tmpFilter = tmpFilter[:-1]
            else:
                tmpFilter = ':'.join(splits[:]).replace('"', '')
            tmpFrame[keyDict[xtractedKey]] = tmpFilter
    else:
        if splits[0] == '},' or splits[0] == '}':
            started = False
            endCount += 1
    if not started and endCount == 1:
        df.loc[ind] = tmpFrame
        splitCounter += 1
        if splitCounter >= checkpoint:
            df['raw_com'] = df['com']
            df['com'] = df['com'].apply(cleanHTMLText)
            filename = output_filename + '.' + str(splitNumber) + '.csv'
            output_pointer = open(filename, 'w')
            df.to_csv(output_pointer, index=False)
            output_pointer.close()
            print("Split %d saved in %0.2f minutes" %(splitNumber, ((time.time() - b) / 60)))
            b = time.time()
            splitNumber += 1
            splitCounter = 0
            df = pd.DataFrame(columns=columns)
            ind = -1
            fileTell.write("Split %d saved in %0.2f minutes\n" %(splitNumber -
                                                                 1,
                                                                 ((time.time()
                                                                   - b) / 60)))
            fileTell.write("File pos: " + str(file.tell()) + '\n')
            fileTell.write("At record: " + str(overall_record + 1) + '\n\n\n')

        ind += 1
        overall_record += 1
        # Maybe do checkpointing
        print("\tAt record: " + str(overall_record) + ' ', end='\r')
if started:
    print("\nDone! But with hanging records")
else:
    print("\nDone completely!")

# Store leftovers
df['raw_com'] = df['com']
df['com'] = df['com'].apply(cleanHTMLText)
filename = output_filename + '.' + str(splitNumber) + '.csv'
output_pointer = open(filename, 'w')
df.to_csv(output_pointer, index=False)
output_pointer.close()

print("Split %d saved in %0.2f minutes" %(splitNumber, ((time.time() - b) / 60)))
print("\tAt record: " + str(overall_record) + ' ', end='\r')
print("Job finished in %0.2f minutes" % ((time.time() - a) / 60))
fileTell.close()
file.close()
