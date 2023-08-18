import argparse
import subprocess
import string
import random
import re

class Mac:
    
    address = ""

    
    def get_random_mac_address():
        """Generate and return a MAC address in the format of Linux"""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        mac_str = ':'.join(['{:02x}'.format(byte) for byte in mac])
        return mac_str
    
    def get_current_mac_address(iface):
    # use the ifconfig command to get the interface details, including the MAC address
        output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
        return re.search("ether (.+) ", output).group().split()[1].strip()
    
    def change_mac_address(iface, new_mac):
        # disable the network interface
        subprocess.check_output(f"ifconfig {iface} down", shell=True)
        # change the MAC
        subprocess.check_output(f"ifconfig {iface} hw ether {new_mac}", shell=True)
        # enable the network interface again
        subprocess.check_output(f"ifconfig {iface} up", shell=True)




if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Python Mac Changer on Linux")
    # Add arguments
    parser.add_argument("-i", "--interface", type=str, required=True, help="interface to change its mac address")
    parser.add_argument("-r", "--random", action="store_true", help="generate a random MAC address")
    parser.add_argument("-m", "--mac", type=str,  help="new mac address")

    
    args = parser.parse_args()
    iface = args.interface #interface name
    current_mac = Mac.get_current_mac_address(iface)
    print("[*] Current MAC address:", current_mac)
    new_mac = ""
    
    if args.random or len(args.random) == 0 and len(args.mac) == 0:
        new_mac = Mac.get_random_mac_address()
    elif args.mac:
        new_mac = args.mac

    
    Mac.change_mac_address(iface, new_mac)
    new_mac = Mac.get_current_mac_address(iface)
    print("[*] New MAC address:", new_mac)





