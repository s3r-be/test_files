# follow.py
#
# Follow a file like tail -f.

import time
import csv

# create generator that yields line
# generators can be iterated through only once 
def follow(thefile):
    thefile.seek(0,2) # 0 is offset, 2 is whence (relative to file end)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line # return line 

if __name__ == '__main__':
    logfile = open("file.csv","r")
    loglines = follow(logfile) # create object of the generator
    # for loop runs the generator code in every iteration
    # once it reaches yield, it returns the line
    for line in loglines:
        print(len(list(csv.reader([line]))[0]))