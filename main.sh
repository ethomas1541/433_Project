#!/bin/bash

# Exit if no argv[1]
[ -z "$1" ] && echo "Usage: ./main.sh [IPv4 address of nameserver] [OPTIONAL: URL for domain]"
[ -z "$1" ] && exit

# NOTE: LATENCY IS ALWAYS CLIENT-TO-NAMESERVER. Can't reliably remotely calculate latency between 2 remote servers

mode=0                      # Mode 0 is client to nameserver

[ ! -z "$2" ] && mode=1     # Mode 1 is nameserver to domain (wherein domain IP arg 2 is specified)

mode_string="CLIENT TO NAMESERVER"

# Make sure both servers are readily ping-able without unreasonable latency

# DNS should be VERY FAST, web domains can have a little more time

timeout 2 ping -c 1 $1 > DNS_ping.txt

if [ "$(wc -l DNS_ping.txt | awk {'print $1'})" -lt 1 ]; then
    echo "Invalid or slow DNS"
    exit
fi

if [ $mode == 1 ]; then
    mode_string="NAMESERVER TO DOMAIN"
    timeout 10 ping -c 1 $2 > domain_ping.txt
    if [ "$(wc -l DNS_ping.txt | awk {'print $1'})" -lt 1 ]; then
        echo "Invalid or slow domain"
        exit
    fi
fi

# Set up dump file
printf "DNS INFO FOR $1:\n\n" > dump.txt

delv @$1 > delv_out.txt

DNSSEC=$(cat delv_out.txt | grep validated)

rm delv_out.txt

if [ "$DNSSEC" = "; fully validated" ]; then
    printf "NAMESERVER: DNSSEC ENABLED\n\n" >> dump.txt
else
    printf "NAMESERVER: UNSIGNED RESPONSE\n\n" >> dump.txt
fi

printf "TIME\t\tLATENCY\t\tROUTER HOPS ($mode_string)\n" >> dump.txt

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