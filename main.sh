#!/bin/bash

# Exit if no argv[1]
[ -z "$1" ] && echo "Usage: ./main.sh [IPv4 address of nameserver] [OPTIONAL: URL for domain]"
[ -z "$1" ] && exit

# NOTE: LATENCY IS ALWAYS CLIENT-TO-NAMESERVER. Can't reliably remotely calculate latency between 2 remote servers

mode=0                      # Mode 0 is client to nameserver

[ ! -z "$2" ] && mode=1     # Mode 1 includes domain data

# Make sure both servers are readily ping-able without unreasonable latency

# DNS should be VERY FAST, web domains can have a little more time

timeout 2 ping -c 1 $1 > DNS_ping.txt

if [ "$(wc -l DNS_ping.txt | awk {'print $1'})" -lt 1 ]; then
    echo "Invalid or slow DNS"
    exit
fi

if [ $mode == 1 ]; then
    timeout 10 ping -c 1 $2 > domain_ping.txt
    if [ "$(wc -l DNS_ping.txt | awk {'print $1'})" -lt 1 ]; then
        echo "Invalid or slow domain"
        exit
    fi
fi

rm *txt

# Set up dump file
printf "DNS INFO FOR $1:\n\n" > dump.txt

delv @$1 > delv_out.txt

DNSSEC=$(cat delv_out.txt | grep validated)
NS_secure=0
domain_DNSSEC=""

# Check for domain RSSIG signature
if [ $mode == 1 ]; then
    delv @$1 $2 > delv_out2.txt
    domain_DNSSEC=$(cat delv_out2.txt | head -n 1)
fi

# echo $domain_DNSSEC

# Check for nameserver RRSIG signature
if [ "$DNSSEC" = "; fully validated" ]; then
    printf "NAMESERVER: DNSSEC ENABLED\n\n" >> dump.txt
    NS_secure=1
else
    printf "NAMESERVER: DNNSEC NOT EVIDENT\n\n" >> dump.txt
fi

# Check for domain DNSSEC security
if [ $mode == 1 ]; then
    if [ "$domain_DNSSEC" = "; fully validated" ]; then
        # BOTH nameserver and domain run DNSSEC
        printf "DOMAIN: DNSSEC ENABLED\n\n" >> dump.txt
    else
        if [ $NS_secure = 1 ]; then
            printf "DOMAIN: DNSSEC NOT ENABLED\n\n" >> dump.txt
        else
            # Test the domain against another DNS nameserver (which is KNOWN to run DNSSEC)
            # There's a chance the domain is secure but the given nameserver is not
            delv @8.8.8.8 $2 > delv_out3.txt
            if [ "$(cat delv_out3.txt | head -n 1)" = "; fully validated" ]; then
                printf "DOMAIN: DNSSEC enabled, but incompatible with provided nameserver!\n\n" >> dump.txt
            else
                printf "DOMAIN: DNSSEC NOT ENABLED\n\n" >> dump.txt
            fi
        fi
    fi
fi

rm delv_out*

printf "TIME\t\tLATENCY\t\tROUTER HOPS (CLIENT TO NAMESERVER)\n" >> dump.txt

# Set hop tracker running
./hops.sh $1 &
hops_pid=$!

start_time=$(date +%s)
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
    cur_time=$(date +%s)
    if [ $SECONDS -ge 60 ]; then
        kill $hops_pid
        exit
    fi
done