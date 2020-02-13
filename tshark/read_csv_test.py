# coding: utf-8

import pandas as pd
import csv
from io import StringIO

# test_string = "'15','Feb 12, 2020 22:21:35.988503395 IST','66','98:22:ef:d5:cc:2f','68:ff:7b:9c:eb:36','192.168.0.104','172.217.27.194','6','52','0','34182','443','34182 → 443 [ACK] Seq=65 Ack=2 Win=501 Len=0 TSval=1539233138 TSecr=3242423058'"

# df = pd.DataFrame(list(test_string))

# print(list(csv.reader([test_string], quotechar="'"))[0])

# print(pd.read_csv(StringIO(test_string.decode('utf-8', 'ignore')), quotechar="'", header=None))

# print(pd.read_csv(StringIO(line.decode('utf-8', 'ignore')), header=None))

# print(pd.DataFrame([test_string.split(',')]))

test = '18|Feb 13, 2020 19:19:07.458232429 IST|66|98:22:ef:d5:cc:2f|68:ff:7b:9c:eb:36|192.168.0.104|151.101.129.69|6|52|0|35532|443|35532 → 443 [ACK] Seq=47 Ack=47 Win=947 Len=0 TSval=2769369778 TSecr=963893469'

split_test = test.split('|')
print(len(split_test))