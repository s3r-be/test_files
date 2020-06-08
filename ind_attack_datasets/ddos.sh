#!/bin/bash

echo 'Enter target ip address: '
read targetIp

for i in {1..10}
do 
	gnome-terminal -- ping $targetIp	
done
