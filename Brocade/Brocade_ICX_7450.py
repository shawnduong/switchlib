# Brocade ICX 7450

class Brocade_ICX_7450:
	"""
	A single Brocade ICX 7450 switch.
	"""

	# Configuration object.
	config = None

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

		# Load the logging function.
		self.log = output.log

		# Load the config.
		self.config = config

		# Load IP address.
		self.ip = ip

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

			self.log("Attempting to connect to switch via SSH.", self.ip, self.config.output, self.config.suppress)

			self.connection = netmiko.ConnectHandler(
				global_delay_factor=4,
				ip=self.ip,
				device_type="ruckus_fastiron",
				username=username,
				password=password,
				secret=secret)

			self.connection.enable()
			self.connected = True

			self.log("SSH connection successfully established.", self.ip, self.config.output, self.config.suppress)

			return 0

		# Bad login credentials.
		except netmiko.ssh_exception.AuthenticationException:

			self.log("SSH connection failed. Bad credentials.", self.ip, self.config.output, self.config.suppress)

			self.connection  = None
			self.connected   = False

			return -1

		# Other bad error.
		except Exception as error:

			self.log(f"Could not connect to switch via SSH. Another error occurred.", self.ip)
			traceback.print_exc()

			self.connection  = None
			self.connected   = False

			return -2

