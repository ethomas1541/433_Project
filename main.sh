#!/bin/bash

# Exit if no argv[1]
[ -z "$1" ] && echo "Usage: ./main.sh [IPv4 address of nameserver] [OPTIONAL: IPv4 address of domain]"
[ -z "$1" ] && exit

# Set up dump file
printf "DNS INFO FOR $1:\n\nTIME\t\tLATENCY\t\tROUTER HOPS\n" > dump.txt

# Set hop tracker running
./hops.sh $1 &

while true
do
    sleep 1
    printf "$(date '+%H:%M:%S')\t$(ping -c 1 $1 | grep time | head -n 1 | awk {'print $7'} | cut -b 6-)\t\t" >> dump.txt
    hopcount=$(tail -n 2 hopdump.txt | head -n 1 | awk {'print $2'})
    hop_msg="AWAITING"
    if [ "$hopcount" != "HOPS" ]; then
        hop_msg=$hopcount
    fi
    printf "$hop_msg\n" >> dump.txt
done