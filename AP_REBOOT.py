#!/usr/bin/python3

#Script to go through and reboot all of the aps in a network and add a delay in if needed.

#imports
import requests
import re
import time

#Private credentials file, used to make life easy when I deploy new scripts.
import cred

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key

REGEX = re.compile("MR")

#Main URL for the Meraki Platform
dashboard = "https://api.meraki.com/api/v0"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#Pull back the networks based on org

#Pull the information from the Meraki cloud to get the network id
#pull back all of the networks for the organization
get_network_id_url = dashboard + '/organizations/%s/networks' % organization

#request the network data
get_network_id_response = requests.get(get_network_id_url, headers=headers)

#puts the data into json format
get_network_id_json = get_network_id_response.json()

cleannetworks = {}
for network in get_network_id_json:
    for key, value in network.items():
        if key == 'id':
            net_id = value
        elif key == 'name':
            net_name = value
        else:
            continue
    cleannetworks[(net_name)] = {'netid': (net_id)}

#prints out the names of the networks so you can choose.
for y in cleannetworks:
    print("Please choose the name of the network you would like to reboot the APs for")
    print(y)

NETWORKNAME = input("Which network? ")
DELAY = int(input("Delay between the reboots(enter time in seconds)? "))


for x in cleannetworks:
    if NETWORKNAME == x:
        NETWORK_ID = (cleannetworks[NETWORKNAME]["netid"])
    else:
        continue

#grab the device in the network and then go through and then reboot them.
get_device_id_url = dashboard + '/networks/%s/devices' % NETWORK_ID
get_device_id_response = requests.get(get_device_id_url, headers=headers)
get_device_id_json = get_device_id_response.json()

for DEVICE in get_device_id_json:
    if REGEX.match(DEVICE["model"]):
        device_id = DEVICE['serial']
        reboot_device_url = dashboard + '/networks/%s/devices/%s/reboot' % (NETWORK_ID, device_id)
        reboot_device_response = requests.post(reboot_device_url, headers=headers)
        print("APs are being rebooted with a " + (DELAY) + " delay.")
        print(DEVICE['name'] + " rebooted")
        #no matter what time delay just to make sure that we don't hit any api errors.
        time.sleep(1)
        #manually chosen delay from above.
        time.sleep((DELAY))

print("All APs in the network have been rebooted")