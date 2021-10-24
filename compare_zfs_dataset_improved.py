#!/usr/bin/env python3

import os
import re
import sys
from colorama import Fore
ZPOOL="/usr/sbin/zpool"
ZFS="/usr/sbin/zfs"
LOCAL_ZFS_POOL="127.0.0.1"
REMOTE_ZFS_POOL="52.168.180.71"
ZFS_FIELDS="logicalused,compressratio,compression,used,recordsize"

# =================================================
# Initialize dictionaries
# =================================================
dict_a = {}
dict_b = {}


# =================================================
# Process file 1
# =================================================
#data_1 = os.popen(f'zfs get -H { ZFS_FIELDS }')
# substitute "NEW_LOCAL.txt" for a much larger file to read/parse/process
with open("NEW_LOCAL.txt") as data_1:
	for row in data_1:
	    vol_name, prop, value = row.split()[0:3]
	
	    if vol_name not in dict_a:
	       dict_a[vol_name] = {}
	
	    if prop in ZFS_FIELDS:
	       dict_a[vol_name][prop] = value

# =================================================
# Process file 2
# =================================================
#data_2 = os.popen(f'ssh root@{REMOTE_ZFS_SERVER} {ZFS} get -H { ZFS_FIELDS }')
# substitute "NEW_REMOTE.txt" for a much larger file to read/parse/process
with open("NEW_REMOTE.txt") as data_2:
	for row in data_2:
	    vol_name, prop, value = row.split()[0:3]
	
	    if vol_name not in dict_b:
	       dict_b[vol_name] = {}
	
	    if prop in ZFS_FIELDS:
	       dict_b[vol_name][prop] = value

# =================================================
# Create an intersection of both dictionary keys
# =================================================
intersection_keys = dict_a.keys() & dict_b.keys()

# =================================================
# Print out comparison data
# =================================================
def display_data(dataset):
	#print(dataset)
	#sys.exit()
	print(Fore.WHITE)
	print()
	print(f"ZFS Volume: {dataset}")
	print("===========================================================")
	print("                         Local           Remote            ")
	print("===========================================================")
	for field in ZFS_FIELDS.split(","):
		a=dict_a[dataset][field]
		b=dict_b[dataset][field]

		field_string=field + ":"
		field_string="{0:<25}".format(field_string)

		a_string="{0:<15}".format(a)
		b_string="{0:<15}".format(b)
		if a == b:
			print(Fore.WHITE + field_string,a_string,b_string)
		else:
			print(Fore.YELLOW + field_string,a_string,b_string,"   < --- NOT SAME")



# ========================================================
# Main here
# ========================================================
arguments=len(sys.argv) - 1

if arguments == 0:
	# --------------------------------------------
	# No arguments passed - listing all datasets
	# --------------------------------------------
	for line in intersection_keys:
		display_data(line)
else:
	# --------------------------------------------
	# Cycle through the arguments and try to match
	# a dataset with an argument using wildcards
	# --------------------------------------------
	position=1
	while (arguments >= position):
		arg=[sys.argv[position]]
		if not any(arg[0] in word for word in intersection_keys):
			print(f"No matching dataset for: {arg[0]}")

		else:
			for line in [match for match in intersection_keys if str(arg[0]) in match]:
				display_data(line)
		position += 1 


# ================================
# Reset the console colors
# ================================
print(Fore.RESET, end="")

sys.exit()


# ========================
# End of Script
# ========================
