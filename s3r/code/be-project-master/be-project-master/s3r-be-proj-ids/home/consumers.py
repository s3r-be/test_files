from channels.generic.websocket import WebsocketConsumer
import json
import time
import os
import pickle
import sklearn
import pandas as pd

# specify file name of machine learning model - pickle file
filename = 'home/model2.txt'
infile = open(filename, 'rb')
rf_model = pickle.load(infile)

# attack type dictionary - key -> prediction, value -> attack type
attack_type = {
    0: 'Normal',
    1: 'Wrong Setup',
    2: 'DDOS',
    3: 'Data Type Probing',
    4: 'Scan Attack',
    5: 'MITM'
}

# ---------------------------------------------------------------------------------------- chat consumer - network logs


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    # Follow a file like tail -f.
    # create generator that yields line
    # generators can be iterated through only once
    def follow(self, thefile):
        thefile.seek(0, 2)  # 0 is offset, 2 is whence (relative to file end)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line  # return line

    # receive request and start a loop to send network data back
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Returns the Path your .py file is in
        workpath = os.path.dirname(os.path.abspath(__file__))
        logfile = open(os.path.join(workpath, "file.csv"), "r")

        # check if file.csv is populated, number of lines should be greater than 1
        while(len([line for line in logfile]) <= 1):
            continue

        loglines = self.follow(logfile)  # create object of the generator
        # for loop runs the generator code in every iteration
        # once it reaches yield, it returns the line

        for line in loglines:
            line = line.split('$')
            # line contains data separated with $
            # the number of columns is 13
            # however some dataframes will show len < 13 because the data is written incompletely by tshark
            # every few seconds 1 dataframe will be dropped

            if len(line) == 13:
                self.send(text_data=json.dumps({
                    'frame.number': line[0],
                    'frame.time': line[1],
                    'frame.len': line[2],
                    'eth.src': line[3],
                    'eth.dst': line[4],
                    'ip.src': line[5],
                    'ip.dst': line[6],
                    'ip.proto': line[7],
                    'ip.len': line[8],
                    'tcp.len': line[9],
                    'tcp.srcport': line[10],
                    'tcp.dstport': line[11],
                    '_ws.col.Info': line[12]
                }))
# ----------------------------------------------------------------------------- end of chat consumer

# ----------------------------------------------------------------------------- attack notif - notifications page


class attackNotif(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    # Follow a file like tail -f.
    # create generator that yields line
    # generators can be iterated through only once
    def follow(self, thefile):
        thefile.seek(0, 2)  # 0 is offset, 2 is whence (relative to file end)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line  # return line

    # receive request and start a loop to send network data back
    def receive(self, text_data):

        # previous values to check if attack logging is being repeated
        prev_mac_source = ''
        prev_mac_dest = ''
        prev_prediction = 0

        # receive message sent from front end
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Returns the Path your .py file is in
        workpath = os.path.dirname(os.path.abspath(__file__))
        logfile = open(os.path.join(workpath, "file.csv"), "r")

        # check if file.csv is populated, number of lines should be greater than 1
        while(len([line for line in logfile]) <= 1):
            continue

        loglines = self.follow(logfile)  # create object of the generator
        # for loop runs the generator code in every iteration
        # once it reaches yield, it returns the line

        for line in loglines:
            returnLog = line  # storing in temp var to return as log
            line = line.split('$')
            # line contains data separated with $
            # the number of columns is 13
            # however some dataframes will show len < 13 because the data is written incompletely by tshark
            # every few seconds 1 dataframe will be dropped

            if len(line) == 13:

                line[1] = line[1].split(' ')[3].replace(
                    ':', '').replace('.', '')  # pre time
                line[3] = int(line[3].replace(':', ''), 16)  # pre eth src
                line[4] = int(line[4].replace(':', ''), 16)  # pre eth dst
                try:
                    line[5] = float(line[5].replace('.', ''))  # pre ip src
                except Exception as ex:
                    line[5] = 0
                try:
                    line[6] = float(line[6].replace('.', ''))  # pre ip dst
                except Exception as ex:
                    line[6] = 0
                try:
                    line[7] = int(line[7])  # pre protocol
                except Exception as ex:
                    line[7] = -1
                try:
                    line[8] = int(line[8])  # pre ip length
                except Exception as ex:
                    line[8] = 0
                try:
                    line[9] = int(line[9])  # tcp length
                except Exception as ex:
                    line[9] = 0
                try:
                    line[10] = int(line[10])  # tcp source port
                except Exception as ex:
                    line[10] = 0
                try:
                    line[11] = int(line[11])  # tcp destination port
                except Exception as ex:
                    line[11] = 0
                value = -99
                if(line[-1].startswith("GET / HTTP/1.1 ")):
                    value = -99
                elif (line[-1].startswith("GET")):  # wrong setup and data type probing
                    a = line[-1].split("=")
                    try:  # if = hasn't been read, index 1 doesn't exist
                        b = (a[1].split(" "))
                        try:
                            # check if float data is sent, if string it is data type probing
                            value = float(b[0])
                        except Exception as ex:
                            value = -3
                    except Exception as ex:
                        value = -99
                elif(line[-1].startswith("Echo")):  # ddos
                    value = -2
                elif (line[-1].startswith("Who")):  # scan
                    value = -4

                elif "duplicate " in line[-1]:  # mitm
                    value = -5
                else:
                    value = -99
                line[-1] = value

                ip_df = pd.DataFrame([line[1:]])
                # get classification - attack or normal
                prediction = rf_model.predict(ip_df)[0]
                if prediction != 0:
                    # print('attack: ' + str(prediction))
                    # still a string to this point
                    returnLog = returnLog.split('$')

                    # check if attack is being repeated for same mac source and dest
                    if not (prev_mac_source == returnLog[3] and prev_mac_dest == returnLog[4] and prev_prediction == prediction):

                        self.send(text_data=json.dumps({
                            'attack.type': attack_type[prediction],
                            'frame.number': returnLog[0],
                            'frame.time': returnLog[1],
                            'frame.len': returnLog[2],
                            'eth.src': returnLog[3],
                            'eth.dst': returnLog[4],
                            'ip.src': returnLog[5],
                            'ip.dst': returnLog[6],
                            'ip.proto': returnLog[7],
                            'ip.len': returnLog[8],
                            'tcp.len': returnLog[9],
                            'tcp.srcport': returnLog[10],
                            'tcp.dstport': returnLog[11],
                            '_ws.col.Info': returnLog[12]
                        }))
                        # set prev values - to prevent overloading of front end
                        prev_mac_source = returnLog[3]
                        prev_mac_dest = returnLog[4]
                        prev_prediction = prediction

# --------------------------------------------------------------------------------------- end of attack notif
