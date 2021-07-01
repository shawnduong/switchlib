# Brocade ICX 7450

class Brocade_ICX_7450:
	"""
	A single Brocade ICX 7450 switch.
	"""

	# Configuration object.
	config = None

	# Logging function.
	log = None

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

		from _common import common

		# Load the config.
		self.config = config

		# Load IP address.
		self.ip = ip

		# Load the logging function.
		self.log = lambda msg: common.log(msg, self.ip, self.config.output, self.config.suppress)

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

	def send_cmd(self, cmd, expect=None, sensitive=False):
		"""
		Send a command to the switch and return the output. The expect string is
		the string of characters at which to stop scanning for output.
		"""

		import traceback

		if not sensitive:
			self.log(f"Sending command: {cmd}")
		else:
			self.log(f"Sending command: <COMMAND NOT SHOWN: This command contains sensitive data.>")

		# Try to send the command and receive a raw response.
		try:

			if expect:
				output = self.connection.send_command(cmd, expect_string=expect)
			else:
				output = self.connection.send_command(cmd)

		# Other bad error.
		except:

			self.log(f"Could not send command to switch. Another error occurred.")
			traceback.print_exc()

			return -1

		self.log("Command successfully sent. Response:")

		# Output the response.
		for line in output.split("\n"):
			self.log(f"| {line}")

		return output

	def config_mode_enter(self):
		"""
		Enter config mode.
		"""

		import traceback

		self.log("Entering config mode.")

		# Try to start config mode.
		try:
			self.connection.config_mode()
		except:
			self.log("Could not enable config mode. Another error occurred.")
			traceback.print_exc()
			return -1

		self.log("Config mode enabled.")

		return 0

	def config_mode_exit(self):
		"""
		Exit config mode.
		"""

		import traceback

		self.log("Exiting config mode.")

		# Try to exit config mode.
		try:
			self.connection.exit_config_mode()
		except:
			self.log("Could not disable config mode. Another error occurred.")
			traceback.print_exc()
			return -1

		self.log("Config mode disabled.")

		return 0

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

	def tacacsp_setup(self, ips, key, enable=True):
		"""
		Add TACACS+ servers using the servers' IP addresses. Return 0 if success,
		or a negative if failed. The key is required to be passed. For convenience,
		enabling password for authentication is also able to be done here.
		"""

		# If only adding one IP given str, turn it into a single-member list.
		if type(ips) is str:
			ips = [ips]

		self.log(f"Preparing to add {len(ips)} TACACS+ server%s." % ("s" if len(ips) != 1 else ""))

		# Enter config mode.
		self.config_mode_enter()

		# aaa authentication web-server default tacacs+ local
		if self.send_cmd("aaa authentication web-server default tacacs+ local") == -1:
			return -2

		# aaa authentication login default tacacs+ local (optional: enable)
		if enable:
			if self.send_cmd("aaa authentication login default tacacs+ local enable") == -1:
				return -3
		else:
			if self.send_cmd("aaa authentication login default tacacs+ local") == -1:
				return -4

		# aaa authorization exec default tacacs+
		if self.send_cmd("aaa authorization exec default tacacs+") == -1:
			return -5

		# tacacs-server host <ip> (for all IPs)
		for ip in ips:

			self.log(f"Adding TACACS+ server {ip}.")

			if self.send_cmd(f"tacacs-server host {ip}") == -1:
				return -6

		self.log("Adding TACACS server key.")

		# tacacs-server key <key>
		if self.send_cmd(f"tacacs-server key {key}", None, True) == -1:
			return -7

		# Exiting config mode.
		self.config_mode_exit()

		return 0

	def tacacsp_config_enable(self, vlanid):
		"""
		Enable the VLAN filter for a given VLAN ID.
		"""

		self.log(f"Enabling the VLAN filter on VLAN ID {vlanid}")

		# Enter config mode.
		self.config_mode_enter()

		if self.send_cmd(f"tacacs-server enable vlan {vlanid}") == -1:
			return -1

		# Exit config mode.
		self.config_mode_exit()

		return 0

	def tacacsp_config_retransmit(self, n):
		"""
		Set the number of retries before giving up to n.
		"""

		self.log(f"Setting the number of TACACS+ server retries to {n}.")

		# Enter config mode.
		self.config_mode_enter()

		if self.send_cmd(f"tacacs-server retransmit {n}") == -1:
			return -1

		# Exit config mode.
		self.config_mode_exit()

		return 0

	def tacacsp_config_timeout(self, n):
		"""
		Set the server timeout to n seconds.
		"""

		self.log(f"Setting the TACACS+ server timeout to {n} second%s." % ("s" if n != 1 else ""))

		# Enter config mode.
		self.config_mode_enter()

		if self.send_cmd(f"tacacs-server timeout {n}") == -1:
			return -1

		# Exit config mode.
		self.config_mode_exit()

		return 0

