import subprocess
import fileinput
import os
import sys


def install_prereqs():
	project_path = os.path.dirname(os.path.abspath(__file__))
	
	os.system('clear')
	os.system('apt update')
	os.system('clear')
	os.system('apt install python3 bundler libsqlite3-dev isc-dhcp-server hostapd libxml2-dev libxslt-dev -y')
	os.system('clear')
	os.system('gem install nokogiri --no-document -v 1.6.6.2 -- --use-system-libraries')
	os.system('clear')
	os.system('bundle install --gemfile=' + project_path + '/Configuration\ App/Gemfile')
	os.system('clear')

def update_config_paths():
	project_path = os.path.dirname(os.path.abspath(__file__))

	os.system('sudo cp -a Reset\ Device/static_files/rc.local.aphost.template Reset\ Device/static_files/rc.local.aphost')
	os.system('sudo cp -a Reset\ Device/static_files/rc.local.apclient.template Reset\ Device/static_files/rc.local.apclient')
	os.system('sudo cp -a Reset\ Device/reset.py.template Reset\ Device/reset.py')
	os.system('sudo cp -a Reset\ Device/manual_reset.py.template Reset\ Device/manual_reset.py')

	with fileinput.FileInput("Reset Device/static_files/rc.local.aphost", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/static_files/rc.local.apclient", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/reset.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close
		
	with fileinput.FileInput("Reset Device/manual_reset.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close


#################################################################
#################################################################

os.system('clear')
print()
print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
install_ans = input("Would you like run the initial RaspiWiFi setup (This can take up to 5 minutes)? (y/n): ")

if(install_ans == 'y'):
	install_prereqs()
	update_config_paths()

	os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f ./tmp/*')
	os.system('sudo cp -a ./Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
	os.system('sudo cp -a ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
	os.system('sudo cp -a ./Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
	os.system('sudo cp -a ./Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
	os.system('sudo cp -a ./Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("RaspiWiFi installation cancelled. Nothing changed...")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	sys.exit()

os.system('clear')
print()
print()
print("#####################################")
print("##### RaspiWiFi Setup Complete  #####")
print("#####################################")
print()
print()
print("Initial setup is complete. A reboot is required to start in WiFi configuration mode...")
reboot_ans = input("Would you like to do that now? (y/n): ")

if reboot_ans == 'y':
	os.system('sudo reboot')
