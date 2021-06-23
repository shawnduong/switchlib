# Brocade ICX 7450

class Brocade_ICX_7450:
	"""
	A single Brocade ICX 7450 switch.
	"""

	# Configuration object.
	config = None

	# Logging function and standard args.
	log = None
	std = None

	# IP address.
	ip = None

	# Connection status and object.
	connection  = None
	connected   = None

	def __init__(self, mode="ic", ip=None, config=None, username=None, password=None, secret=None):
		"""
		Constructor method.

		Available modes:
		"n"    => instantiate only.
		"i"    => initialize.
		"ic"   => i, connect.
		"""

		# Instantiate only.
		if mode == "n":
			pass

		# Initialize.
		if mode == "i":
			self.init(ip, config)

		# Connect.
		if mode == "ic":
			self.init(ip, config)
			self.connect(username, password, secret)

	def init(self, ip, config):
		"""
		Initialize a switch with metadata.
		"""

		import sys
		sys.path.insert(0, "../")

		from _common import output

		# Load the config.
		self.config = config

		# Load IP address.
		self.ip = ip

		# Load the logging function.
		self.log = lambda msg: output.log(msg, self.ip, self.config.output, self.config.suppress)

		# Haven't connected to switch yet.
		self.connected = False

		return 0

	def connect(self, username, password, secret):
		"""
		Spawn a connection via SSH.
		"""

		import netmiko
		import traceback

		# Load an SSH connection into self.connection.
		try:

			self.log("Attempting to connect to switch via SSH.")

			self.connection = netmiko.ConnectHandler(
				global_delay_factor=4,
				ip=self.ip,
				device_type="ruckus_fastiron",
				username=username,
				password=password,
				secret=secret)

			self.connection.enable()
			self.connected = True

			self.log("SSH connection successfully established.")

			return 0

		# Bad login credentials.
		except netmiko.ssh_exception.AuthenticationException:

			self.log("SSH connection failed. Bad credentials.")

			self.connection  = None
			self.connected   = False

			return -1

		# Other bad error.
		except:

			self.log(f"Could not connect to switch via SSH. Another error occurred.")
			traceback.print_exc()

			self.connection  = None
			self.connected   = False

			return -2

	def send_cmd(self, cmd, expect=None):
		"""
		Send a command to the switch and return the output. The expect string is
		the string of characters at which to stop scanning for output.
		"""

		import traceback

		self.log(f"Sending command: {cmd}")

		# Try to send the command and receive a raw response.
		try:

			if expect:
				output = self.connection.send_command(cmd, expect_string=expect)
			else:
				output = self.connection.send_command(cmd)

		# Other bad error.
		except:

			self.log(f"could not send command to switch. another error occurred.")
			traceback.print_exc()

			return -1

		self.log("command successfully sent. response:")

		# Output the response.
		for line in output.split("\n"):
			self.log(f"| {line}")

		return output

	def ping(self, ip):
		"""
		Ping another device from the switch using the device's IP address. Return the
		latency in seconds, or -1 if timed out.
		"""

		import re

		self.log(f"Pinging {ip}.")

		# Send the command and parse it for latency.
		if (output := self.send_cmd(f"ping {ip}")) != -1:

			# Return the time in seconds as an output.
			if len(q := re.findall("time=(\d+)ms", output)) > 0:
				return float(q[0]) / 1000

		# Default return is only reached in case of a timeout.
		return -1
