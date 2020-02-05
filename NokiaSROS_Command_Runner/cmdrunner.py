

##Credit to (https://www.youtube.com/watch?v=eiYemtNKS-M&list=PLtw40n4ybvFoHoigW7IwITNilmZn2cfNv)
##Reworked to work with netmiko 3.0.0
##This is based for Nokia SROS, but can easily be changed to support any OS NetMiko supports



from __future__ import absolute_import, division, print_function

import json
import logmein      ##External logmein script
import netmiko.ssh_exception
from netmiko import Netmiko
from netmiko import ConnectHandler
import os
import signal
import sys


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


if len(sys.argv) < 4:
    print('Usage Example: cmdrunner.py showcommands.txt admindisplayconfig.txt nokia_nodes.json')   ##this Script #commands in a list #device type and login type
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = logmein.get_credentials()     #calls imported custom library function for user login


with open(sys.argv[1]) as cmd_file:                 #first argument, list of commands to run
    commands = cmd_file.readlines()

with open(sys.argv[2]) as shrun_file:               #second argument, admin display-config, usually every large that is why its in a seperate file
    shruns = shrun_file.readlines()

with open(sys.argv[3]) as node_file:                #dictionary info of node/host to pass to netmiko for connection handeling
    nodes = json.load(node_file)
    hostname = (nodes[0]['host'])                   #passed dictonary line for description of file output


output_path = '/XXXs/XXX/XXX/NetMiko_Command_Runner/NokiaSROS_Netmiko/output/'   #where you want the output
filename_cmd = os.path.join(output_path, hostname+'-ShowCommands.txt')           #name your show command file               
filename_shrun = os.path.join(output_path, hostname+'-AdminDisplay.txt')         #name your admin display-config file


for node in nodes:                                                  #passed variables from logmein.py
    node['username'] = username
    node['password'] = password
    try:
        print('~' * 79)
        print('Connecting to device:', node['host'])
        net_connect = Netmiko(**node)
        for command in commands:                                        #show run commands start here
            output1 = (command + '\n')
            output2 = (net_connect.send_command(command) + '\n')
            with open(filename_cmd, 'a') as out_file1:
                out_file1.write(output1 + output2)
                out_file1.close
        for shrun in shruns:                                            #admin display-config starts here
            output3 = (shrun + '\n')
            output4 = (net_connect.send_command(shrun) + '\n')
            with open(filename_shrun, 'a') as out_file2:
                out_file2.write(output3 + output4)
                out_file2.close
        net_connect.disconnect()
        print('Success! Check output file for results')
    except netmiko_exceptions as error:
        print('Failed to ', node['host'], error)
