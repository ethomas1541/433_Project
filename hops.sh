printf "HOPS TO $1\n\nTIME\t\tHOPS\n" > hopdump.txt

while true
do
    printf "$(date '+%H:%M:%S')\t" >> hopdump.txt
    expr $(traceroute $1 | wc -l) - 1 >> hopdump.txt
done