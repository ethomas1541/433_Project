printf "HOPS TO $1\n\nTIME\t\tHOPS\tROUTER IPs\n" > hopdump.txt

while true
do
    traceroute $1 > rt.txt
    printf "\n$(date '+%H:%M:%S')\t$(expr $(cat rt.txt | wc -l) - 1)\t\t" >> hopdump.txt
    cat rt.txt | grep -Po "^(?:.*?)\((?:\d{1,3}\.){3}\d{1,3}" | grep -Po "(?<=\().*" | tail -n +2 | tr '\n' ' '>> hopdump.txt
done