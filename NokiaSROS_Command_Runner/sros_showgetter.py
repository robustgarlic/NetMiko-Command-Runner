

##Credit to (https://www.youtube.com/watch?v=eiYemtNKS-M&list=PLtw40n4ybvFoHoigW7IwITNilmZn2cfNv)
##Reworked to work with netmiko 3.0.0
##This is based for Nokia SROS, but can easily be changed to support any OS NetMiko supports






from io import StringIO
import json
import userinput    #custom additional inputs
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

print(Fore.WHITE + '\n*************' + Fore.CYAN +  ' Nokia SROS show_getter v1.1 ' + Fore.WHITE + '************')
print(Fore.RED + '\nUsage Example:' + Fore.CYAN + 'sros_showgetter.py ShowCommands.txt nokia_inventory.json')

## Define Usage ##
if len(sys.argv) < 3:
    print(Fore.WHITE + '\n' + '*' * 27)
    print('\n')
    print(Fore.RED + 'Try Again. Usage Example:' + Fore.CYAN +  'sros_showgetter.py ShowCommands.txt nokia_inventory.json')   ##this Script #commands in a list #device type and login type
    print('\n')
    print(Fore.WHITE + '*' * 27)
    print('\n')
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

## variables called from custom script ##
username, password = userinput.get_credentials()
hostname = userinput.get_host()



## read show commands ##
with open(sys.argv[1]) as cmd_file:
    commands = cmd_file.readlines()
## reads json disctory of nodes ##
with open(sys.argv[2]) as node_file:
    nodes = json.load(node_file)

## define file names, file paths ##
output_path = '/XXXX/Test-7750-Show-Getter/output'
filename_cmd = os.path.join(output_path, hostname+'-outputcommands.txt')



## function to run commands ##
def command_runner():
    for node in nodes:
        node['username'] = username
        node['password'] = password
        node['host'] = hostname
        try:
            print(Fore.WHITE + '\n' + '~' * 79)
            print(Fore.CYAN + 'CONNECTING TO DEVICE:' + Fore.WHITE+ node['host'])
            net_connect = Netmiko(**node)
            s = StringIO()  #fake file because im terrible
            for command in commands:
                output1 = ('\n' + command)
                output2 = ('\n' + net_connect.send_command(command))
                s.write(output1 + output2) # fake file 
                gatheroutput = s.getvalue() # get fake file stuff
                user_message = (Fore.MAGENTA + "\nRUNNING COMMANDS: " + Fore.WHITE + command.strip()) # prints commands and output to the user
                print(user_message)
                print(output2)
            return gatheroutput # return fake file to real file write function
            net_connect.disconnect()
        except netmiko_exceptions as error:
            print('\n' * 2)
            print('Failed to ', node['host'], error)
            print('\n' * 2)
            sys.exit()

## function to write file based on user input ##
## checks if file already exists, asks user to overwrite ##
def file_writer(gatheroutput):
            header = ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' + hostname + '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            while True:
                print(Fore.WHITE+ '\nNOW WE WRITE THE OUTPUT')
                if os.path.isfile(filename_cmd):
                     overwrite_pre = input(Fore.WHITE + "\nThe **OUTPUT file already exists. Overwrite? y = yes, n = no: ").lower()
                     if overwrite_pre == 'y':
                            with open(filename_cmd, "a") as file:
                                file.write(header + '\n')
                                file.write(gatheroutput)
                                file.close()
                                print(Fore.WHITE + '\n**OUTPUT FILE FINISHED WRITING, CHECK OUTPUT FOLDER')
                                break
                        elif overwrite_pre == 'n':
                            print(Fore.RED + '\nInvalid Input: ' + Fore.WHITE + 'You have selected NO. Try again.')
                        else:
                            print(Fore.RED + '\nInvalid Input: ' + Fore.WHITE + 'Try again.')
                 else:
                     print(Fore.CYAN +  '\nWRITING' + Fore.WHITE + '**OUTPUT FILE....')
                     with open(filename_cmd, "a") as file:
                         file.write(header + '\n')
                         file.write(gatheroutput)
                         file.close()
                         print(Fore.WHITE + '\n**OUTPUT FILE FINISHED WRITING, CHECK OUTPUT FOLDER')
                         break

if __name__ == "__main__":
    gatheroutput = command_runner()
    file_writer(gatheroutput)
