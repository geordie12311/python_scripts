import threading
#import paramiko
import subprocess
import getpass
import sys
import time
import os
import getopt
import socket
from sys import argv
from nornir import InitNornir
from nornir_scrapli.tasks import send_commands_from_file
from rich import print as rprint
from nornir_salt.plugins.functions import FFun #importing FFun from salt for filtering hosts
from nornir_utils.plugins.functions import print_result #importing print_result to print the results to screen

nr = InitNornir(config_file="config.yaml")

# Promt symbol
prompt = '\t# '

def clear_screen():
    os.system('clear')

def pause():
	print("\n")
	programPause = input('\tPress the <ENTER> key to continue...')
	print("\n")

def main_menu():
	clear_screen()
	print('\n\n')
	print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * *')
	print('\t*    ______  __       _______.  ______   ______         *')
	print('\t*   /      ||  |     /       | /      | /  __  \        *')
	print('\t*  |  ,-----|  |    |   (----`|  ,-----|  |  |  |       *')
	print('\t*  |  |     |  |     \   \    |  |     |  |  |  |       *')
	print('\t*  |  `----.|  | .----)   |   |  `----.|  `--`  |       *')
	print('\t*   \______||__| |_______/     \______| \______/        *')
	print('\t*    ______   ______   .__   __.  _______               *')
	print('\t*   /      | /  __  \  |  \ |  | |   ____|              *')
	print('\t*  |  ,----`|  |  |  | |   \|  | |  |__                 *')
	print('\t*  |  |     |  |  |  | |  . `  | |   __|                *')
	print('\t*  |  `----.|  `--`  | |  |\   | |  |                   *')
	print('\t*   \______| \______/  |__| \__| |__|                   *')
	print('\t* * * * * * * * * * * * * * * * * * * * * * * * * * * *')
	print('\n\n\t Choose number wisely:\n\n')
	print('\t\t1. Input host names (comma seperated): ')
	print('\t\t2. Load commands to be executed from file\n')
	print('\t\t3. Show commands that was loaded from file\n')
	print('\t\t4. Submit your credentials\n')
	print('\t\t5. Start executing commands in every IP address in your file')
	print('\n\n\t\tq. Quit')
	choice = input('\n\n >> ')
	if choice == "1":
		get_hosts()
	elif choice == "2":
		get_cmds_file()	
	elif choice == "3":
		show_cmds_from_file()
	elif choice == "4":
		get_user_credentials()
	elif choice == "5":
		start_cmds_to_ip_from_file()
	elif choice == "q":
		quit()
	else:
		print("invalid selection")


def get_hosts():
    print("\tEnter the hostnames of the devices, (comma seperated): ")
    targets = input(prompt)

def get_cmds_file():
	try:
		print("\tEnter commands file name: ")
		cmds = input(prompt)
		f = open(cmds,'r')
	except IOError:
		print("\tThere is no such file")
		pause()
	else:
		print("\tFile successfully loaded")
		f.close()
		pause()
		
def show_cmds_from_file():
	try:
		myfile = open(cmds, 'r')
		print("\tCommands to be executed: \n")
		for cmd in myfile:
			cmd = cmd.strip('\n')
			print("\t" , cmd)
		pause()
	except:
		print("\tNo file with commands to be executed has been loaded\n")
		pause()
		get_cmds_file()
		
	
def get_user_credentials():
    username = input("Enter your username: ")
    print("\tEnter Password: ")
    password = getpass.getpass('\tPassword:')
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = password
    
def check_user_credentials():
	try:
		if username or password != "":
			print("\tCredentials are loaded\n")
	except:
		print("\tNo credentials loaded yet\n")
		get_user_credentials()

def start_cmds_to_ip_from_file():
	check_user_credentials()
	print("\tWe are about to connect to these \n")
	get_hosts()
	print("\tAnd we will submit \n")
	show_cmds_from_file()
	choice = ""
	while choice != "y" or "n":
		print("\tYou are going to start connecting in your routers and execute commands, are you sure? (y) or (n)?")
		choice = input('\t\n\n >> ')
		if choice == "n":
			main_menu()
		else:
			print("\t please choose 'y' or 'n' ")
			pause()
		break

def send_commands():
	target = input(targets) #using user inputted hosts details for targets
	cmds_to_send = input(cmds) # using user inputted commands to send to hosts
	
filtered_hosts = FFun(nr, FL=target) # using FFun filter to filter the hosts
output = filtered_hosts.run(send_commands_from_file, file="myfile") #splitting the commands using the comma as the delimiter

results = (output) #creating results object to capture output from the task
print_result(results) #printing out the results from the task

while True:
	main_menu()