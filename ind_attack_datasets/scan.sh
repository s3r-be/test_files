#!/bin/bash

for i in {1..10}
do
	gnome-terminal -- nmap 192.168.0.*
done
