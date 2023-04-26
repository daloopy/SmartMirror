import subprocess
from user import *
import os


def connect_to_wifi():
	print("connecting to wifi...")
	user = User()
	network_name = user.get_user_wifi_name()
	network_password = user.get_user_wifi_password()
	
	print("connecting to ", network_name)
	
	os.system('sudo systemctl stop wpa_supplicant.service') # stop any previously running service
	os.system('sudo rm /var/run/wpa_supplicant/wlan0') # remove any previous wlan0 configurations
	os.system('sudo systemctl stop wpa_supplicant-nl80211@p2p-dev-lan0.service') # stop that previous wlan0 service we removed
	
	with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
		f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
		f.write('update_config=1\n')
		f.write('country=us\n')
		f.write('p2p_disabled=1\n\n')
		f.write('network={\n')
		f.write(f'\tssid="{network_name}"\n')
		f.write(f'\tpsk="{network_password}"\n')
		f.write('}\n')
	
	os.system('sudo systemctl restart networking.service')
	os.system(f'sudo wpa_supplicant -B -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0')
	os.system('sudo dhclient wlan0')

def is_internet_connected():
	try:
		subprocess.check_call(['ping', '-c', '1', '8.8.8.8'])
		return True
	except subprocess.CalledProcessError:
		return False
		
def wait_for_connection():
	while not is_internet_connected():
		pass

def connect_to_wifi_userpass():
	print("connecting to wifi...")
	user = User()
	network_name = user.get_user_wifi_name()
	network_username = user.get_user_wifi_username()
	network_password = user.get_user_wifi_userpassword()
	
	print("connecting to ", network_name)
	
	os.system('sudo systemctl stop wpa_supplicant.service') # stop any previously running service
	os.system('sudo rm /var/run/wpa_supplicant/wlan0') # remove any previous wlan0 configurations
	os.system('sudo systemctl stop wpa_supplicant-nl80211@p2p-dev-lan0.service') # stop that previous wlan0 service we removed
	
	with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
		f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
		f.write('update_config=1\n')
		f.write('country=us\n')
		f.write('p2p_disabled=1\n\n')
		f.write('network={\n')
		f.write(f'\tssid="{network_name}"\n')
		f.write('\tkey_mgmt=WPA-EAP\n')
		f.write('\teap=PEAP\n')
		f.write('\tidentity="{network_username}"\n')
		f.write('\tpassword="{network_password}"\n')
		f.write('\tphase2="auth=MSCHAPV2"\n')
		f.write('}\n')
	
	os.system('sudo systemctl restart networking.service')
	os.system(f'sudo wpa_supplicant -B -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0')
	os.system('sudo dhclient wlan0')


connect_to_wifi_userpass()
wait_for_connection()
print("connected")