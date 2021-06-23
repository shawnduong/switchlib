#!/usr/bin/env python3

import sys
sys.path.insert(0, "../../")

from _common import output

def test_log(args):

	if len(args) == 4:
		args[-1] = True if args[-1].startswith("T") else False

	output.log(*args)

def main(args):

	# Help menu.
	if len(args) == 0:

		print("Manual Common Tests")
		print("'o' means optional.")
		print("log            ./test_common log <MESSAGE> <oIP> <oOUTPUT> <oSUPPRESS: 'T' || 'F'>")

		return -1

	# Test log.
	if args[0] == "log":
		test_log(args[1::])

if __name__ == "__main__":
	main(sys.argv[1::])
