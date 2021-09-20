# Firewalld Management

import os
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

CONF = {}

console = Console()

def gpr(string):
	console.print(Text(string,style="bold green"))

def rpr(string):
	console.print(Text(string,style="bold red"))

def menu():
	print("\t..............Menu..........................")
	gpr("\t1.Status of firewall")
	gpr("\t2.Set Rules")
	gpr("\t3.Delete Rules")
	gpr("\t4.Exit")

def fw_activate():
	print("...........Activating the firewall...........")
	os.popen("sudo systemctl start firewalld").read() # starting firewall

def fw_get_status():
	cmd="sudo firewall-cmd --state" # checking firewall status
	state = os.popen(cmd).read()
	if state == "running\n":
		gpr("Firewall is active")
	else:
		rpr("Firewall is not active")
		fw_activate()
	fw_get_active_zones()	

def fw_get_active_zones():
	print("\t..............Getting Active Zones..................")
	zone = os.popen("sudo firewall-cmd --get-active-zones").read() # getting active zones
	CONF["ZONE"] = zone.split("\n")[0]
	print(CONF)


def get_zone_list():
	print("................Getting all zone list.....................")
	zone_lst = os.popen("sudo firewall-cmd --get-zones").read().split(" ") # listing zones
	zone_lst[-1]=zone_lst[-1][:-1]
	return zone_lst

def fw_reload():
	 print(os.popen("sudo firewall-cmd --reload").read())

def fw_list_all(zone):
	cmd_lst = "sudo firewall-cmd --list-all --zone="+zone+" --permanent" # listing the details
	print(os.popen("sudo firewall-cmd --list-all --zone="+zone+" --permanent").read())

def fw_add_port():
	print("...................Adding Port.....................")
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-port="+port_no+"/"+proto+" --zone="+zone+" --permanent" # adding port
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)

def fw_get_services():
	print(".....Service List.....")
	cmd = "sudo firewall-cmd --get-services" # listing the services
	print(os.popen(cmd).read()) 

def fw_add_services():
	fw_get_services()
	fw_get_active_zones()
	print("..................Adding Service................")
	service = Prompt.ask("Enter service name from the above list :")
	zone = Prompt.ask("Enter the zone",choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-service="+service+" --zone="+zone+" --permanent" # adding services
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)	

def fw_add_source_port():
	print(".............Adding Source Port..................")
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-source-port="+port_no+"/"+proto+" --zone="+zone+" --permanent" # adding source port
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)

def fw_add_sources():
	print(".............Adding Source..................")
	port_no = Prompt.ask("Enter the port number")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-source="+port_no+" --zone="+zone+" --permanent" # adding sources
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)

def fw_set_rules_menu():
	print("\t..............Set Rules Menu.................")
	gpr("\t1.Add Port")
	gpr("\t2.Add Services")
	gpr("\t3.Add Sources")
	gpr("\t4.Add  Source Port")
	gpr("\t5.Back to Main Menu")


def fw_set_rules():
	fw_set_rules_menu()
	ch = Prompt.ask("Enter your choice :",choices=["1","2","3","4","5"])
	if ch == "1":
		fw_add_port()
	elif ch == "2":
		fw_add_services()
	elif ch == "3":
		fw_add_sources()
	elif ch == "4":
		fw_add_source_port()
		
	elif ch == "5":
		menu()
	else:
		rpr("\tWrong choice")

def fw_delete_port():
	print(".............Deleting Port................")
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-port="+port_no+"/"+proto+" --zone="+zone+" --permanent" # deleting the port
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)
	
def fw_delete_services():
	print("..............Deleting Services................")
	fw_get_services()
	fw_get_active_zones()
	service = Prompt.ask("Enter service name from the above list :")
	zone = Prompt.ask("Enter the zone",choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-service="+service+" --zone="+zone+" --permanent" # deleting the service
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)

def fw_delete_source_port():
	print("..................Deleting Source Port................")
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-source-port="+port_no+"/"+proto+" --zone="+zone+" --permanent" # deleting the source port
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)

def fw_delete_sources():
	print("..................Deleting Sources................")
	port_no = Prompt.ask("Enter the port number")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-source="+port_no+ " --zone="+zone+ " --permanent" # deleting the source
	print(os.popen(cmd).read())
	fw_reload()
	fw_list_all(zone)


def fw_delete_rules_menu():
	print("\t..........Delete Rules Menu................")
	rpr("\t1.Delete Port")
	rpr("\t2.Delete Services")
	rpr("\t3.Delete Sources")
	rpr("\t4.Delete Source Port")
	rpr("\t5.Back to Main Menu")


def fw_delete_rules():
	fw_delete_rules_menu()
	ch = Prompt.ask("Enter your choice :",choices=["1","2","3","4"])
	if ch == "1":
		fw_delete_port()
	elif ch == "2":
		fw_delete_services()
	elif ch == "3":
		fw_delete_sources()
	elif ch == "4":
		fw_delete_source_port()
	elif ch == "5":
		menu()
	else:
		rpr("\tWrong choice")


if __name__ == "__main__":
	while True:
		menu()
		ch = Prompt.ask("\tEnter your choice :",choices=["1","2","3","4"])
		if ch == "1":
			fw_get_status()
		elif ch == "2":
			fw_set_rules()
		elif ch == "3":
			fw_delete_rules()
		elif ch == "4":
			break
		else:
			rpr("\tWrong choice")


