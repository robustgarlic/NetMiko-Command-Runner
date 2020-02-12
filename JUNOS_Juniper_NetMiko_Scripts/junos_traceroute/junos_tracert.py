from __future__ import absolute_import, division, print_function

import logmein      #custom un and password
import userinput    #custom additional inputs
import netmiko.ssh_exception
from netmiko import Netmiko
from netmiko import ConnectHandler
import os
import signal
import sys



signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


if len(sys.argv) < 2:
    print('\n' * 2)
    print('Usage Example: junos_tracert.py  juniper_inventory.json')   ##this Script #commands in a list #device type and login type
    print('\n' * 2)
    exit()


with open(sys.argv[1]) as node_file:
    nodes = json.load(node_file)

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)


username, password = logmein.get_credentials()
hostname = userinput.get_host()
vrf = userinput.get_vrf()
ipaddress = userinput.get_ipaddr()



for node in nodes:
    node['username'] = username
    node['password'] = password
    node['host'] = hostname
    try:
        print('Connecting to device:', node['host'])
        net_connect = Netmiko(**node)
        command = ('traceroute routing-instance {} {}'.format(vrf,ipaddress))
        output = (net_connect.send_command(command))
        print('\n' * 2)
        print (output)
        print('\n' * 2)
        net_connect.disconnect()
        break
    except netmiko_exceptions as error:
        print('\n' * 2)
        print('Failed to ', node['host'], error)
        print('\n' * 2)
        break

