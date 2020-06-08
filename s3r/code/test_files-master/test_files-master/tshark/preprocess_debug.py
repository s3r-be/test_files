import pandas as pd
data = '1$Feb 16, 2020 12:37:22.736684743 IST$54$50:02:91:69:66:71$98:22:ef:d5:cc:2f$192.168.0.35$192.168.0.121$6$40$0$49279$80$GET /ids/server.php?data=kachra HTTP/1.1'

line = data.split('$')
print('line: ', end='')
print(line)

pre_time = line[1].split(' ')[3].replace(':', '').replace('.', '')
line[1] = int(pre_time)
print('time: ' + str(pre_time))

pre_eth_src = int(line[3].replace(':', ''), 16)
line[3] = pre_eth_src
print('eth src: ' + str(pre_eth_src)) 

pre_eth_dst = int(line[4].replace(':', ''), 16)
line[4] = pre_eth_dst
print('eth dst: ' + str(pre_eth_dst))

pre_ip_src = line[5].replace('.', '')
line[5] = int(pre_ip_src)
print('ip src: ' + str(pre_ip_src))

pre_ip_dst = line[6].replace('.', '')
line[6] = int(pre_ip_dst)
print('ip dst: ' + str(pre_ip_dst))

value = -99
if(line[-1].startswith("GET / HTTP/1.1 ")):
    value = -99
elif (line[-1].startswith("GET")):  ###### wrong setup and data type probing
    a = line[-1].split("=")
    b = (a[1].split(" "))
    try:
        value = float(b[0])
    except:
        value = -3
elif(line[-1].startswith("Echo")):  ######### ddos
    value = -2
elif (line[-1].startswith("Who")):  ############# scan 
    value = -4
    
elif "duplicate " in line[-1]:      ############# mitm
    value = -5
else:
    value = -99
print('value: ' + str(value))
line[-1] = value

ip_df = pd.DataFrame([line[1:]])
print(ip_df)
print(ip_df.dtypes)