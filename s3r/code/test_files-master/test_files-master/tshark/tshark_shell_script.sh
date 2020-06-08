#!/bin/bash

echo s3rbeproj | sudo -S `#to get sudo permissions`\
tshark `#run tshark`\
-T fields -e frame.number -e frame.time -e frame.len -e eth.src -e eth.dst `#give fields to capture`\
-e ip.src -e ip.dst -e ip.proto -e ip.len -e tcp.len -e tcp.srcport -e tcp.dstport -e _ws.col.Info \
-E header=y -E separator="$" -E quote=n -E occurrence=f `#set headers, separator as comma, double quotations, first occurrence`\
> file.csv `#dump into file.csv`\
-i wlp3s0 `#interface wifi`