data = 'GET /ids/server.php?data=attack HTTP/1.1'
dataNoEq = 'GET /ids/server.php?data'
nexxt = dataNoEq.split('=')
the = nexxt[1].split('')
print(nexxt)