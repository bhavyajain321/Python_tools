#!/usr/bin/env python3
#made with python3


import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "-target", dest="target", help="Target Ip /.Ip range.")
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    #arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    #arp_request_broadcast.show()
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP()) 
    # scapy.ls(scapy.Ether()) 
    #print(arp_request_broadcast.summary())
    answered_list = scapy.srp(arp_request_broadcast, timeout=4, verbose=False)[0]
    # print(answered.summary())

   
    clients_list = []
    for element in answered_list:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(clients_dict)
        
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n--------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)