# advanced preprocessing

from cleaning import Cleaning

class Preprocessing(Cleaning):
    
    # attack type dictionary - key -> prediction, value -> attack type
    attack_type = {
        0: 'Normal',
        1: 'Wrong Setup',
        2: 'DDOS',
        3: 'Data Type Probing',
        4: 'Scan Attack',
        5: 'MITM'
    }
    # frequency of attacks assigned in normality
    assignedAttacks = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    # dictionary used for storing time stamp and frequency per eth src
    ddosDict = {}
    scanDict = {}
    mitmDict = {}

    def __init__(self):
        super(Preprocessing, self).__init__()

        self.colLength = len(self.df['frame.number'])
        self.new_columns()
        self.wrong_setup_dtp()
        self.ddos()
        self.scan()
        self.mitm()

        print('ddosDict', self.ddosDict)
        print('scanDict', self.scanDict) 
        print('mitmDict', self.mitmDict)
        print('attack frequency in dataset - ')
        [print('{0:25}'.format(self.attack_type[key]), value) for (key, value) in sorted(self.assignedAttacks.items())]

        

    def new_columns(self):
        try:
            # create new column for int info initiated to -99
            self.df['info'] = [ -99 for i in range(self.colLength) ]
            print('[DONE] create new column for int info initiated to -99')
        except:
            print('[FAIL] create new column for int info initiated to -99')

        try:
            # create new column for normality initiated to 0
            self.df['normality'] = [ 0 for i in range(self.colLength) ]
            print('[DONE] create new column for normality initiated to 0')
        except:
            print('[FAIL] create new column for normality initiated to 0')

    def wrong_setup_dtp(self):
        try:
            # set correct info and normality codes
            for ind in range(self.colLength):

                colInfo = self.df.loc[ind, '_ws.col.Info']

                # WRONG SETUP / DATA TYPE PROBING
                if (colInfo.startswith("GET")):  
                    splitByEq = colInfo.split("=")
                    try:  # if = hasn't been read, index 1 doesn't exist
                        splitBySp = (splitByEq[1].split(" "))
                        try:
                            # check if float data is sent, if string it is data type probing
                            value = float(splitBySp[0])
                            if value == 0:
                                self.df.loc[ind, 'normality'] = 1
                                self.assignedAttacks[1] += 1
                        except:
                            value = -3
                            self.df.loc[ind, 'normality'] = 3
                            self.assignedAttacks[3] += 1
                    except:
                        value = -99
                    self.df.loc[ind, 'info'] = value
            print('[DONE] set correct info and normality codes - WRONG SETUP / DATA TYPE PROBING')
        except:
            print('[FAIL] set correct info and normality codes - WRONG SETUP / DATA TYPE PROBING')
    
    def ddos(self):
        ddosDict = {}
        try:
            for ind in range(self.colLength):
                colInfo = self.df.loc[ind, '_ws.col.Info']
                if colInfo.startswith("Echo"):
                    timeStamp = self.df.loc[ind, 'frame.time']
                    ethSrc = self.df.loc[ind, 'eth.src']
                    if ethSrc in ddosDict:  # check if eth src in ddos dict
                        # if yes, check if time diff is greater than 2 sec
                        if timeStamp - ddosDict[ethSrc][0] > 2000000000 and ddosDict[ethSrc][1] > 100:
                            value = -2  # ddos attack detected
                            # update timestamp and frequency
                            ddosDict[ethSrc] = [timeStamp, 0]
                            self.df.loc[ind, 'normality'] = 2
                            self.assignedAttacks[2] += 1
                        else:  # if diff less than 2 sec
                            ddosDict[ethSrc][1] += 1  # update frequency
                    else:  # eth src not in ddosDict
                        value = -99  # pass - reduntant detection
                        # create dict record for eth src with time stamp, frequency as value
                        ddosDict[ethSrc] = [timeStamp, 0]
                    self.df.loc[ind, 'info'] = value
            print('[DONE] set correct info and normality codes - DDOS')
            self.ddosDict = ddosDict
        except:
            print('[FAIL] set correct info and normality codes - DDOS')
    
    def scan(self):
        scanDict = {}
        try:
            for ind in range(self.colLength):
                colInfo = self.df.loc[ind, '_ws.col.Info']
                if colInfo.startswith("Who"):
                    timeStamp = self.df.loc[ind, 'frame.time']
                    ethSrc = self.df.loc[ind, 'eth.src']
                    if ethSrc in scanDict:  # check if eth src in scan dict
                        # if yes, check if time diff is greater than 2 sec
                        if timeStamp - scanDict[ethSrc][0] > 2000000000 and scanDict[ethSrc][1] > 150:
                            value = -4  # scan attack detected
                            # update timestamp and frequency
                            scanDict[ethSrc] = [timeStamp, 0]
                            self.df.loc[ind, 'normality'] = 4
                            self.assignedAttacks[4] += 1
                        else:  # if diff less than 2 sec
                            scanDict[ethSrc][1] += 1  # update frequency
                    else:  # eth src not in scanDict
                        value = -99  # pass - reduntant detection
                        # create dict record for eth src with time stamp, frequency as value
                        scanDict[ethSrc] = [timeStamp, 0]
                    self.df.loc[ind, 'info'] = value
            self.scanDict = scanDict
            print('[DONE] set correct info and normality codes - SCAN')
        except:
            print('[FAIL] set correct info and normality codes - SCAN')

    def mitm(self):
        try:
            for ind in range(self.colLength):
                colInfo = self.df.loc[ind, '_ws.col.Info']
                if "duplicate" in colInfo:
                    value = -5
                    self.df.loc[ind, 'info'] = value
                    self.assignedAttacks[5] += 1
            print('[DONE] set correct info and normality codes - MITM')
        except:
            print('[FAIL] set correct info and normality codes - MITM')
                


if __name__ == '__main__':
    oPreprocessing = Preprocessing()
    oPreprocessing.test()