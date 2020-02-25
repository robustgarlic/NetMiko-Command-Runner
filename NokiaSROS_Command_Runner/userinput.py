
import sys
import os
import signal
from getpass import getpass
from colorama import init
from colorama import Fore
import ipaddress


def get_input(prompt=''):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_credentials():
    """Prompt for and return a username and password."""
    print(Fore.WHITE + '\n' + '*' * 48)
    username = get_input('\n\nEnter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match.  Try again.')
            password = None
    return username, password
    
def get_host():
    """Prompt for Hostname to pass on to Netmiko Dictionary"""
    print(Fore.WHITE + '\n' + '*' * 48)
    host_device = input('What is the hostname of the target device?: ')
    host_verify = input('Verify hostname of target device: ')
    if (host_device != host_verify):
        print(Fore.WHITE + '\n' + '*' * 48)
        print('\nHostnames do not match. Rerun Script Again.')
        print(Fore.WHITE + '\n' + '*' * 48)
        sys.exit()
    else:
        return host_device


def get_ipaddr():
    """Prompt for IP Address to pass as variable"""
    print(Fore.WHITE + '\n' + '*' * 48)
    ipaddr = input('Input IP Address, e.g. 10.10.10.0 : ')
    while True:
        if(ipaddress.ip_address(ipaddr)==False):
            print(Fore.WHITE + '\n' + '*' * 48)
            print("This is an invalid address.")
            print(Fore.WHITE + '\n' + '*' * 48)
            sys.exit()
        else:
            print(Fore.WHITE + '\n' + '*' * 48)
            print('IP address {} is valid'.format(ipaddr))
            print(Fore.WHITE + '\n' + '*' * 48)
            return ipaddr

