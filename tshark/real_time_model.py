import pickle
import sklearn
import time
import pandas as pd

filename = 'model2.txt'
infile = open(filename,'rb')
rf_model = pickle.load(infile)

# Follow a file like tail -f.
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
        print(line[0])
        line[1] = line[1].split(' ')[3].replace(':', '').replace('.', '') # pre time
        line[3] = int(line[3].replace(':', ''), 16) # pre eth src
        line[4] = int(line[4].replace(':', ''), 16) # pre eth dst
        try:
            line[5] = float(line[5].replace('.', '')) # pre ip src
        except:
            line[5] = 0
        try:
            line[6] = float(line[6].replace('.', '')) # pre ip dst
        except:
            line[6] = 0 
        try:
            line[7] = int(line[7]) # pre protocol
        except:
            line[7] = -1
        try:
            line[8] = int(line[8]) # pre ip length
        except:
            line[8] = 0
        try:
            line[9] = int(line[9]) # tcp length
        except:
            line[9] = 0
        try:
            line[10] = int(line[10]) # tcp source port
        except:
            line[10] = 0
        try:
            line[11] = int(line[11]) # tcp destination port
        except:
            line[11] = 0
        value = -99
        if(line[-1].startswith("GET / HTTP/1.1 ")):
            value = -99
        elif (line[-1].startswith("GET")):  ###### wrong setup and data type probing
            a = line[-1].split("=")
            try: # if = hasn't been read, index 1 doesn't exist
                b = (a[1].split(" "))
                try:
                    value = float(b[0]) # check if float data is sent, if string it is data type probing
                except:
                    value = -3
            except:
                value = -99
        elif(line[-1].startswith("Echo")):  ######### ddos
            value = -2
        elif (line[-1].startswith("Who")):  ############# scan 
            value = -4
            
        elif "duplicate " in line[-1]:      ############# mitm
            value = -5
        else:
            value = -99
        line[-1] = value

        ip_df = pd.DataFrame([line[1:]])
        prediction = rf_model.predict(ip_df)[0]
        if prediction != 0:
            print ('attack: ' + str(prediction))

