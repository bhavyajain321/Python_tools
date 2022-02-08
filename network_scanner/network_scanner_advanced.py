#/usr/bin/env python
#built with python2

import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target Ip / Ip range.")
    (options, arguments) = parser.parse_args()
    return options
# def scan(ip):
#     scapy.arping(ip)

# scan("192.168.0.1/24")

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  #creating packet  #pdst means ip 
    #print(arp_request.summary())
    #scapy.ls(scapy.ARP()) #give the list of fields
    # arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #creating etherframe from ether
    #print(broadcast.summary())
    #scapy.ls(scapy.Ether()) #give the list of fields
    #broadcast.show()
    arp_request_broadcast = broadcast/arp_request #combining arp_req and broadcast packet together
    #print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    #answered, unanswered = scapy.srp(arp_request_broadcast, timeout=5) #srp for sending and receving packets
    #we use two var answered and unanswered becoz scapy.srp return two values(lists).
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
    #print(answered.summary())
    #print(answered_list.summary())

    #scanning
    clients_list = []
    for element in answered_list:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        #print(element[1].psrc + "\t\t" + element[1].hwsrc)
        clients_list.append(clients_dict)
    return clients_list

#printing the result
def print_result(results_list):
    print("IP\t\t\tMAC Address\n--------------------------------------") #header designing
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
