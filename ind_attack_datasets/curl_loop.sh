#!/bin/bash

ip=$1

for i in {1..1000}
do 
	curl $ip/ids/server.php?data=$i
done
