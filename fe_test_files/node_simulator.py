# importing the requests library
import requests
import time

# api-endpoint
URL = 'http://localhost/ids/server.php'

for i in range(0, 10000, 25):
    # data to be sent
    data = i

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'data': data}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    print('sent data: ', data, '| response code: ', r)

    time.sleep(0.2)
