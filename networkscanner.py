#!/usr/bin/env python

import scapy.all as scapy
import argparse

art = """
                     /$$                                   /$$                                                                     
                    | $$                                  | $$                                                                     
 /$$$$$$$  /$$$$$$ /$$$$$$  /$$  /$$  /$$ /$$$$$$  /$$$$$$| $$   /$$ /$$$$$$$ /$$$$$$$ /$$$$$$ /$$$$$$$ /$$$$$$$  /$$$$$$  /$$$$$$ 
| $$__  $$/$$__  $|_  $$_/ | $$ | $$ | $$/$$__  $$/$$__  $| $$  /$$//$$_____//$$_____/|____  $| $$__  $| $$__  $$/$$__  $$/$$__  $$
| $$  \ $| $$$$$$$$ | $$   | $$ | $$ | $| $$  \ $| $$  \__| $$$$$$/|  $$$$$$| $$       /$$$$$$| $$  \ $| $$  \ $| $$$$$$$| $$  \__/
| $$  | $| $$_____/ | $$ /$| $$ | $$ | $| $$  | $| $$     | $$_  $$ \____  $| $$      /$$__  $| $$  | $| $$  | $| $$_____| $$      
| $$  | $|  $$$$$$$ |  $$$$|  $$$$$/$$$$|  $$$$$$| $$     | $$ \  $$/$$$$$$$|  $$$$$$|  $$$$$$| $$  | $| $$  | $|  $$$$$$| $$      
|__/  |__/\_______/  \___/  \_____/\___/ \______/|__/     |__/  \__|_______/ \_______/\_______|__/  |__|__/  |__/\_______|__/      
"""

print(art)
print("#" * 130)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Specify the IP / IP range to scan.")
    (options) = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []

    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")

    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
