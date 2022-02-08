pip install netfiltetqueue

IPTABLES RULES:

for victim pc:
iptables -I FORWARD -j NFQUEUE --queue-num 0 

for testing on remote desktop:
iptables -I OUTPUT -j NFQUEUE --queue-num 0 
iptables -I INPUT -j NFQUEUE --queue-num 0 

after work done:
iptables --flush
