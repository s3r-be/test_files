# cleaning + basic pre processing

import pandas as pd
import numpy as np

class Cleaning:

    def __init__(self, CSV_FILE='tshark_1_2_125000.csv'):
        try:
            # read csv file, fill nan with 0
            self.df = pd.read_csv(CSV_FILE, sep='$')
            self.df.fillna(0, inplace=True)
            print('[DONE] read csv file, fill nan with 0')
        except:
            print('[FAIL] read csv file, fill nan with 0')

        try:
            # get only time, remove ':', '.', convert to int
            self.df['frame.time'] = self.df['frame.time'].str.split().str[3].str.replace(':', '').str.replace('.', '').astype(int)
            print('[DONE] get only time, remove \':\', \'.\', convert to int')
        except:
            print('[FAIL] get only time, remove \':\', \'.\', convert to int')

        try:
            # remove ':', convert hex to decimal for eth src and dst
            self.df['eth.src'] = self.df['eth.src'].str.replace(':', '').apply( int, base=16 )
            self.df['eth.dst'] = self.df['eth.dst'].str.replace(':', '').apply( int, base=16 )
            print('[DONE] remove \':\', convert hex to decimal for eth src and dst')
        except:
            print('[FAIL] remove \':\', convert hex to decimal for eth src and dst')

        try:
            # ip src - remove '.', fill nan with 0, convert to int
            self.df['ip.src'] = self.df['ip.src'].str.replace('.', '')
            self.df['ip.src'].fillna(0, inplace=True)
            self.df['ip.src'] = self.df['ip.src'].astype(int)
            print('[DONE] ip src - remove \'.\', fill nan with 0, convert to int')
        except:
            print('[FAIL] ip src - remove \'.\', fill nan with 0, convert to int')
 
        try:
            # ip dst - remove '.', fill nan with 0, convert to int
            self.df['ip.dst'] = self.df['ip.dst'].str.replace('.', '')
            self.df['ip.dst'].fillna(0, inplace=True)
            self.df['ip.dst'] = self.df['ip.dst'].astype(int)
            print('[DONE] ip dst - remove \'.\', fill nan with 0, convert to int')
        except:
            print('[FAIL] ip dst - remove \'.\', fill nan with 0, convert to int')
 
        try:
            # convert following cols to int
            intConv = [ 'ip.proto', 'ip.len', 'tcp.len', 'tcp.srcport', 'tcp.dstport' ]
            self.df[intConv] = self.df[intConv].astype(int)
            print('[DONE] convert cols "ip.proto, ip.len, tcp.srcport, tcp.dstport" to int')
        except:
            print('[FAIL] convert cols "ip.proto, ip.len, tcp.srcport, tcp.dstport" to int')


    def test(self):
        print(self.df.head())
        print(self.df.describe())
        print(self.df.dtypes)
        print(self.df.isnull().sum())

if __name__ == '__main__':
    oCleaning = Cleaning()
    oCleaning.test()