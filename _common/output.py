# Common output definitions.

def log(msg, ip=None, output=None, suppress=False):
	"""
	Logging function.
	"""

	import time

	message = f"[{time.strftime('%Y/%m/%d %H:%M:%S')}] :: %s{msg}\n" % (
		f"({ip}) " if ip != None else "")

	# Write to a file if filename is provided.
	if output:
		with open(output, "a+") as f:
			f.write(message)

	# Output to stdout if not suppressed.
	if not suppress:
		print(message, end="")

	return 0

