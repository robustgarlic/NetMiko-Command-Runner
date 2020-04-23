

##Credit to (https://www.youtube.com/watch?v=eiYemtNKS-M&list=PLtw40n4ybvFoHoigW7IwITNilmZn2cfNv)
##Reworked to work with netmiko 3.0.0
##This is based for Nokia SROS, but can easily be changed to support any OS NetMiko supports


# ┌───────────────────────────────────────────────────────────────────┐
# │                         nokia_sros_show_getter                    │
# ├───────────────────────────────────────────────────────────────────┤
# │ Python script to collect show commands and output them to a file. │
# │ This script also outputs them directly to a webex teams message   │
# │ via a bot. Python3.6+ only.                                       │
# └───────────────────────────────────────────────────────────────────┘




from __future__ import absolute_import, division, print_function


from io import StringIO
import json
import userinput    #customer additional inputs
from colorama import init
from colorama import Fore
import netmiko.ssh_exception
from netmiko import Netmiko
from netmiko import ConnectHandler
from webexteamssdk import WebexTeamsAPI, ApiError #webex sdk library
from datetime import datetime
import os
import signal
import sys

#start time for script
start_time = datetime.now()

##webex stuff
api = WebexTeamsAPI(access_token='your token here, works good with a bot account')

##exception stuff
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


#resets colorama colors#
init(autoreset=True)

#usage header
print(Fore.WHITE + '\n+-------------------------------------------------------------------+' + Fore.CYAN +  '\n|                      Nokia SROS show_getter                       |' + Fore.WHITE + '\n+-------------------------------------------------------------------+')
print(Fore.RED + '\nUsage Example:' + Fore.CYAN + 'sros_showgetter.py commands.txt inventory.json')

## Define Usage if usage fails argument check##
if len(sys.argv) < 3:
    print(Fore.WHITE + '\n' + '*' * 27)
    print('\n')
    print(Fore.RED + 'Try Again. Working Usage Example:' + Fore.CYAN +  'sros_showgetter.py ShowCommands.txt nokia_inventory.json')   ##this Script #commands in a list #device type and login type
    print('\n')
    print(Fore.WHITE + '*' * 27)
    print('\n')
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

## variables called from custom script ##
username, password = userinput.get_credentials()
hostname = userinput.get_host()
webex_email = userinput.get_email()



## read show commands ##
with open(sys.argv[1]) as cmd_file:
    commands = cmd_file.readlines()
## reads json disctory of nodes ##
with open(sys.argv[2]) as node_file:
    nodes = json.load(node_file)

## define file names, file paths ##
pre_output_path = '~/commandrunner/preprocedureoutput'
pre_filename_cmd = os.path.join(pre_output_path, hostname+'-PreProcedureCommands.txt')
post_output_path = '~/commandrunner/postprocedureoutput'
post_filename_cmd = os.path.join(post_output_path, hostname+'-PostProcedureCommands.txt') 


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
            s = StringIO()  #fake file
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
def file_writer(gatheroutput):
            header = ('\n' + '=' * 67 + '\n' + hostname + '\n' + '=' * 67 )
            while True:
                print(Fore.WHITE+ '\nNOW WE WRITE THE OUTPUT')
                preorpost = input("\nPRE or POST Config?: ")
                if preorpost == "PRE":
                    if os.path.isfile(pre_filename_cmd):
                        overwrite_pre = input(Fore.WHITE + "\nThe **PRE Procedure file already exists. Overwrite? y = yes, n = no: ").lower()
                        if overwrite_pre == 'y':
                            with open(pre_filename_cmd, "a") as prefile:
                                prefile.write(header + '\n')
                                prefile.write(gatheroutput)
                                prefile.close()
                                print(Fore.WHITE + '\n**PRE PROCEDURE FILE FINISHED WRITING, CHECK OUTPUT FOLDER')
                                return preorpost
                                break
                        elif overwrite_pre == 'n':
                            print(Fore.RED + '\nInvalid Input: ' + Fore.WHITE + 'You have selected NO. Try again.')
                        else:
                            print(Fore.RED + '\nInvalid Input: ' + Fore.WHITE + 'Try again.')
                    else:
                        print(Fore.CYAN +  '\nWRITING' + Fore.WHITE + '**PRE PROCEDURE FILE....')
                        with open(pre_filename_cmd, "a") as prefile:
                            prefile.write(header + '\n')
                            prefile.write(gatheroutput)
                            prefile.close()
                            print(Fore.WHITE + '\n**PRE PROCEDURE FILE FINISHED WRITING, CHECK OUTPUT FOLDER')
                            return preorpost
                            break
                elif preorpost == "POST":
                    if os.path.isfile(post_filename_cmd):
                        overwrite_post = input(Fore.WHITE + "\nThe **POST Procedure file already exists. Overwrite? y = yes, n = no: ").lower()
                        if overwrite_post == 'y':
                            with open(post_filename_cmd, "a") as postfile:
                                postfile.write(header + '\n')
                                postfile.write(gatheroutput)
                                postfile.close()
                                print(Fore.WHITE + '\n**POST PROCEDURE FILE FINISHED WRITING, CHECK OUTPUT FOLDER')
                                return preorpost
                                break
                        elif overwrite_pre == 'n':
                            print(Fore.RED + '\nInvalid Input: ' + Fore.WHITE + 'You have selected NO. Try again.')
                        else:
                            print(Fore.RED + '\nInvalid Input: ' + Fore.WHITE + 'Try again.')
                    print(Fore.CYAN + '\nWRITING' + Fore.WHITE + '**POST** PROCEDUREFILE\n')
                    with open(post_filename_cmd, "a") as postfile:
                        postfile.write(header + '\n')
                        postfile.write(gatheroutput)
                        postfile.close()
                        print(Fore.WHITE + '\n**POST PROCEDURE FILE FINISHED WRITING, CHECK OUTPUT FOLDER')
                        return preorpost
                        break
                else:
                    print(Fore.RED + '\nINVALID INPUT' + Fore.WHITE + 'PRE OR POST ARE THE ONLY ACCEPTABLE INPUT - TRY AGAIN NEWB.')

##Function for webex output
##sends created file above to inputted user email via 1:1 message
def webexoutput(preorpost):
    print(Fore.MAGENTA + '\n****SENDING FILE TO WEBEX TEAM USER: ' + Fore.CYAN + webex_email)
    while True:
        if preorpost == "PRE":
            try:
                premessage = api.messages.create(toPersonEmail=webex_email, text=('PRE-PROCEDURE FILE for: ' + hostname), files=[pre_filename_cmd])
                print(Fore.CYAN+'\nPRE-PROCEDURE ' + Fore.WHITE + 'output sent to webex teams successfully.')
                break
            except ApiError as e1:
                print(e1)
                break
        elif preorpost == "POST":    
            try:
                postmessage = api.messages.create(toPersonEmail=webex_email, text=('POST-PROCEDURE FILE for: ' + hostname), files=[post_filename_cmd])
                print(Fore.CYAN + '\nPOST-PROCEDURE ' + Fore.WHITE + 'output sent to webex teams successfully.')
                break
            except ApiError as e2:
                print(e2)
                break
        else:
             print(Fore.RED + '\nSOMETHING WENT WRONG:' + Fore.WHITE + 'NO PRE OR POST FILE FOUND, awkward')
             break


#main
if __name__ == "__main__":
    gatheroutput = command_runner()
    preorpost = file_writer(gatheroutput)
    webexoutput(preorpost)
    print("\nElapsed time: " + str(datetime.now() - start_time))
