from __future__ import absolute_import, division, print_function
import sys
import ipaddress



def get_host():
    """Prompt for Hostname to pass on to Netmiko Dictionary"""
    print('\n' * 2)
    print('~' * 79)
    print('\n' * 2)
    host_device = input('What is the hostname of the target device?: ')
    host_verify = input('Verify hostname of target device: ')
    if (host_device != host_verify):
        print('\n' * 2)
        print('Hostnames do not match. Rerun Script Again.')
        print('\n' * 2)
        sys.exit()
    else:
        return host_device

def get_ipaddr():
    """Prompt for IP Address to pass as variable"""
    print('\n' * 2)
    print('~' * 79)
    print('\n' * 2)
    ipaddr = input('Input IP Address, e.g. 10.10.10.0 : ')
    while True:
        if(ipaddress.ip_address(ipaddr)==False):
            print('\n' * 2)
            print("This is an invalid address.")
            print('\n' * 2)
            sys.exit()
        else:
            print('\n' * 2)
            print('IP address {} is valid'.format(ipaddr))
            print('\n' * 2)
            return ipaddr


def get_vrf():
   """Prompt for vrf """
   print('\n' * 2)
   print('~' * 79)
   print('\n' * 2)
   vrf = input('Traceroute from vpn-2 SIP or vpn-3 Internet, : ')
   if vrf == 'vpn-2':
      print('VRF Selected:{}'.format(vrf))
      return vrf
   elif vrf == 'vpn-3':
      print('VRF Selected:{}'.format(vrf))
      return vrf
   else:
    print('Invalid VRF selected, rerun script again and  please select vpn-2 or vpn-3')
        


