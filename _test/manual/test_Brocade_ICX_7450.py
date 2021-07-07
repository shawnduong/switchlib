#!/usr/bin/env python3

import getpass
import sys
sys.path.insert(0, "../../")

from _common import common
from Brocade.Brocade_ICX_7450 import Brocade_ICX_7450

def init(ip, user):
	"""
	Shared switch initialization function returning the device object.
	"""

	conf      = common.config()
	password  = getpass.getpass("(Test) Password: ")
	secret    = getpass.getpass("(Test) Secret: ")

	return Brocade_ICX_7450("ic", ip, conf, user, password, secret)

def test_constructor(args):

	conf = common.config()

	# Instantiate only.
	if len(args) == 0:
		device = Brocade_ICX_7450("n")

	# Initialize only.
	elif len(args) == 1:
		device = Brocade_ICX_7450("i", args[0])

	# Initialize and connect.
	else:
		password  = getpass.getpass("(Test) Password: ")
		secret    = getpass.getpass("(Test) Secret: ")
		device    = Brocade_ICX_7450("ic", args[0], conf, args[1], password, secret)

	print(f"(Test) device.ip         : {device.ip}")
	print(f"(Test) device.connected  : {device.connected}")

def test_send_cmd(args):

	# Initialize and connect.
	device = init(args[0], args[1])

	# Send command.
	if len(args) == 3:
		device.send_cmd(args[2])
	else:
		device.send_cmd(args[2], args[3])

def test_ping(args):

	# Initialize and connect.
	device = init(args[0], args[1])

	# Ping.
	latency = device.ping(args[2])

	print(f"(Test) Latency: {latency}s")

def test_tacacsp_setup(args):

	# Get the key.
	key = getpass.getpass("(Test) Key: ")

	# Initialize and connect.
	device = init(args[0], args[1])

	# Break up the IPs into a list.
	ips = args[2].split(" ")

	# Parse the web-server mode.
	if len(args) > 3:
		wsmode = args[3]
	else:
		wsmode = "tl"

	# Parse the local mode.
	if len(args) > 4:
		lmode = args[4]
	else:
		lmode = "tle"

	# Test TACACS+ setup.
	print(f"(Test) {device.tacacsp_setup(ips, key, wsmode, lmode)}")

def test_tacacsp_config_enable(args):

	# Initialize and connect.
	device = init(args[0], args[1])

	# Enable the VLAN filter using the VLAN ID.
	print(f"(Test) {device.tacacsp_config_enable(args[2])}")

def test_tacacsp_config_retransmit(args):

	# Initialize and connect.
	device = init(args[0], args[1])

	# Set the retransmit to N seconds.
	print(f"(Test) {device.tacacsp_config_retransmit(args[2])}")

def test_tacacsp_config_timeout(args):

	# Initialize and connect.
	device = init(args[0], args[1])

	# Set the timeout to N seconds.
	print(f"(Test) {device.tacacsp_config_timeout(args[2])}")

def main(args):

	# Help menu.
	if len(args) == 0:

		print("Manual Brocade ICX 7450 Tests")
		print("'o' means optional.")
		print("__init__                     ./test_Brocade_ICX_7450.py __init__ <oIP> <oUSER>")
		print("send_cmd                     ./test_Brocade_ICX_7450.py send_cmd <IP> <USER> <CMD> <oEXPECT>")
		print("                                 ? If the command contains spaces, wrap all of <CMD> in quotes.")
		print("ping                         ./test_Brocade_ICX_7450.py ping <IP> <USER> <TARGET_IP>")
		print("tacacsp_setup                ./test_Brocade_ICX_7450.py tacacsp_setup <IP> <USER> <TARGET_IPS> <oWSMODE> <oLMODE>")
		print("                                 ? If there are multiple target IPs, wrap all of <TARGET_IPS> in quotes and separate")
		print("                                   each individual IP using spaces.")
		print("tacacsp_config_enable        ./test_Brocade_ICX_7450.py tacacsp_config_enable <IP> <USER> <VLAN_ID>")
		print("tacacsp_config_retransmit    ./test_Brocade_ICX_7450.py tacacsp_config_retransmit <IP> <USER> <N>")
		print("tacacsp_config_timeout       ./test_Brocade_ICX_7450.py tacacsp_config_timeout <IP> <USER> <N>")

		return -1

	# Test __init__.
	if args[0] == "__init__":
		test_constructor(args[1::])

	# Test send_cmd.
	elif args[0] == "send_cmd":
		test_send_cmd(args[1::])

	# Test ping.
	elif args[0] == "ping":
		test_ping(args[1::])

	# Test tacacsp_setup.
	elif args[0] == "tacacsp_setup":
		test_tacacsp_setup(args[1::])

	# Test tacacsp_config_enable.
	# It is assumed that TACACS+ is already set up.
	elif args[0] == "tacacsp_config_enable":
		test_tacacsp_config_enable(args[1::])

	# Test tacacsp_config_retransmit.
	# It is assumed that TACACS+ is already set up.
	elif args[0] == "tacacsp_config_retransmit":
		test_tacacsp_config_retransmit(args[1::])

	# Test tacacsp_config_timeout.
	# It is assumed that TACACS+ is already set up.
	elif args[0] == "tacacsp_config_timeout":
		test_tacacsp_config_timeout(args[1::])

if __name__ == "__main__":
	main(sys.argv[1::])
