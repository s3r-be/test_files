# coding: utf-8

import pandas as pd
import csv

test_string = "'15','Feb 12, 2020 22:21:35.988503395 IST','66','98:22:ef:d5:cc:2f','68:ff:7b:9c:eb:36','192.168.0.104','172.217.27.194','6','52','0','34182','443','34182 → 443 [ACK] Seq=65 Ack=2 Win=501 Len=0 TSval=1539233138 TSecr=3242423058'"

# df = pd.DataFrame(list(test_string))

print(len(list(csv.reader([test_string]))[0]))

# x = csv.reader([test_string])
# print(pd.DataFrame([test_string.split(',')]))