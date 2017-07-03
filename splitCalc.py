# 
# file = open("test.txt", 'r')
# print(file.readline())
# d = file.tell()
# print(d)
# file.close()
# file = open("test.txt", 'r')
# print(file.tell())
# print(file.readline())
# print(file.readline())
# print(file.readline())
# file.seek(d)
# print(file.readline())
# print(file.tell())
# file.close()


import time

limit = 1600000

file = open('4chan.posts.json', 'r')
# file.readline()
ind = 0
record = 0
print("Processing file.")
started = False
# for i in range(endline):
a = time.time()
endCount = 0
lineCount = 0
file.readline()

seekFile = open('seeker.txt', 'w')
seekPoint = file.tell()
seekFile.write(str(seekPoint) + ',')

while True:
    line = file.readline()
    lineCount += 1
    # the now attribute splits further because of the time syntax
    splits = line.strip().split(":")
    splits = [x.strip() for x in splits]
    if not line:
        break
    if len(splits) > 1 and started == False:
        if splits[1] == '{':
#             print("RECORD STARTED")
            endCount = 0
            started = True
#     elif len(splits) > 1 and started:
#         tmp = ''
# #         print(splits)
    else:
        if splits[0] == '},' or splits[0] == '}':
            started = False
            endCount += 1
    if not started and endCount == 1:
#         print("RECORD ENDED")
#         print(tmpFrame)
        record += 1
        if record >= limit:
            seekPoint = file.tell()
            seekFile.write(str(lineCount) + '\n')
            seekFile.write(str(seekPoint) + ',')
            record = 0
            lineCount = 0
        ind+=1
        # Maybe do checkpointing
        print("\tAt record: " + str(ind) + ' ', end='\r')
#         df.append(tmpFrame)
if started:
    print("\nDone! But with hanging records")
else:
    print("\nDone completely!")
print("Time taken: %0.3f minutes" % ((time.time() - a)/60))
# print("Total lines %d\n" % lineCount)
seekFile.write(str(lineCount) + '\n')
seekFile.close()
with open('report.txt', 'w') as f:
    f.write(str(ind) + '\n')
    f.write("Total lines %d\n" % lineCount)
    f.write(str((time.time() - a)/60) + '\n')
file.close()


