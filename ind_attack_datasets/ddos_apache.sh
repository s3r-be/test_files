#!/bin/bash

# get target ip input from user
echo 'Enter target ip address: (enter d for default ip) - '
read targetIp
if [ "$targetIp" = "d" ] ||  [ "$targetIp" = "D" ] 
then
       targetIp="192.168.0.107"	
fi

# print ip 
echo "ip = $targetIp"

# get absolute path of curl_loop script
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
FILENAME='/curl_loop.sh'
CURL_LOOP=$SCRIPTPATH$FILENAME

# loop to run curl_loop script in new terminal
# pass targetIp
for i in {1..10}
do 
	gnome-terminal -- $CURL_LOOP $targetIp
done
