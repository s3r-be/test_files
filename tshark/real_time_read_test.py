# follow.py
#
# Follow a file like tail -f.

import time
import pandas as pd
from io import StringIO

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
        line = line.split('$') 
        # line contains data separated with $
        # the number of columns is 13
        # however some dataframes will show len < 13 because the data is written incompletely by tshark
        # every few seconds 1 dataframe will be dropped
        if len(line) == 13:
            print(pd.DataFrame([line]))