#!/usr/bin/env python3

import sys
sys.path.insert(0, "../../")

from _common import common

def test_config(args):

	if len(args) == 2:
		args[-1] = True if args[-1].startswith("T") else False

	conf = common.config(*args)

	print(f"conf.output    : {conf.output}")
	print(f"conf.suppress  : {conf.suppress}")

def test_log(args):

	if len(args) == 4:
		args[-1] = True if args[-1].startswith("T") else False

	common.log(*args)

def main(args):

	# Help menu.
	if len(args) == 0:

		print("Manual Common Tests")
		print("'o' means optional.")
		print("config    ./test_common config <oOUTPUT> <oSUPPRESS: 'T' || 'F'>")
		print("log       ./test_common log <MESSAGE> <oIP> <oOUTPUT> <oSUPPRESS: 'T' || 'F'>")

		return -1

	# Test config.
	if args[0] == "config":
		test_config(args[1::])

	# Test log.
	if args[0] == "log":
		test_log(args[1::])

if __name__ == "__main__":
	main(sys.argv[1::])
