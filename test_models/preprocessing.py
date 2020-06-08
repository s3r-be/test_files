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

    def __init__(self):
        super(Preprocessing, self).__init__()

        self.colLength = len(self.df['frame.number'])

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
                        except:
                            value = -3
                            self.df.loc[ind, 'normality'] = 1
                    except:
                        value = -99
                    self.df.loc[ind, 'info'] = value
            print('[DONE] set correct info and normality codes')
        except:
            print('[FAIL] set correct info and normality codes')
                


if __name__ == '__main__':
    oPreprocessing = Preprocessing()
    oPreprocessing.test()