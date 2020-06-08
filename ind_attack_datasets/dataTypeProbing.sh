#!/bin/bash

echo 'Enter target ip: '
read targetIp

count=0

for ((i=1;i<=30000;i++))
do 
	(( count += 1 ))
#	sleep 1 
	curl $targetIp/ids/server.php?data=attack
	echo " -  $count" 
done
