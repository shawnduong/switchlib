#!/usr/bin/env python3

import getpass
import sys
sys.path.insert(0, "../../")

from _common import config
from Brocade.Brocade_ICX_7450 import Brocade_ICX_7450

def test_constructor(args):

	conf = config.config()

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

	print(f"device.ip         : {device.ip}")
	print(f"device.connected  : {device.connected}")

def test_send_cmd(args):

	conf = config.config()

	# Initialize and connect.
	password  = getpass.getpass("(Test) Password: ")
	secret    = getpass.getpass("(Test) Secret: ")
	device    = Brocade_ICX_7450("ic", args[0], conf, args[1], password, secret)

	# Send command.
	if len(args) == 3:
		device.send_cmd(args[2])
	else:
		device.send_cmd(args[2], args[3])

def main(args):

	# Help menu.
	if len(args) == 0:

		print("Manual Brocade ICX 7450 Tests")
		print("'o' means optional.")
		print("__init__    ./test_common __init__ <oIP> <oUSER>")
		print("send_cmd    ./test_common send_cmd <IP> <USER> <CMD> <oEXPECT>")

		return -1

	# Test __init__.
	if args[0] == "__init__":
		test_constructor(args[1::])

	# Test send_cmd.
	if args[0] == "send_cmd":
		test_send_cmd(args[1::])

if __name__ == "__main__":
	main(sys.argv[1::])
