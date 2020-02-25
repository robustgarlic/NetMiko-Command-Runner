
import time
import json
import userinput    #customer additional inputs
from colorama import init
from colorama import Fore
import netmiko.ssh_exception
from netmiko import Netmiko
from netmiko import ConnectHandler
import os
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


#resets colorama colors#
init(autoreset=True)

print(Fore.WHITE + '\n***************' + Fore.CYAN +  ' Simple Traceroute Tool for Junos ' + Fore.WHITE + '**************')
print(Fore.RED + '\nUsage Example:' + Fore.CYAN + 'junos_tracert.py juniper_inventory.json')

## Define Usage ##
if len(sys.argv) < 2:
    print(Fore.WHITE + '\n' + '*' * 34)
    print('\n')
    print(Fore.RED + 'Try Again. Usage Example:' + Fore.CYAN +  'junos_tracert.py juniper_inventory.json')   ##this Script #commands in a list #device type and login type
    print('\n')
    print(Fore.WHITE + '*' * 34)
    print('\n')
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

## reads json disctory of nodes ##
with open(sys.argv[1]) as node_file:
    nodes = json.load(node_file)


## variables called from custom script ##
username, password = userinput.get_credentials()
hostname = userinput.get_host()
vrf = userinput.get_vrf()
ipaddress = userinput.get_ipaddr()



for node in nodes:
    node['username'] = username
    node['password'] = password
    node['host'] = hostname
    try:
        print(Fore.WHITE + '\n' + '~' * 79)
        print(Fore.CYAN + 'CONNECTING TO DEVICE:' + Fore.WHITE+ node['host'])
        print(Fore.RED + '**Keyboard Interrupt ctrl+c')
        net_connect = Netmiko(**node)
        command = ('traceroute routing-instance {} {} ttl 10'.format(vrf,ipaddress)) # command sent using userinput
        user_message = (Fore.MAGENTA + "\nRUNNING COMMAND: " + Fore.WHITE + command) # prints commands and output to the user
        print(user_message)
        print(command)
        net_connect.disconnect()
    except netmiko_exceptions as error:
        print('\n' * 2)
        print('Failed to ', node['host'], error)
        print('\n' * 2)
        break

