# Configuration class.

class config:
	"""
	General configuration options.
	"""

	output    = None
	suppress  = None

	def __init__(self, output="./output.log", suppress=False):
		"""
		Constructor method.
		"""

		self.output    = output
		self.suppress  = suppress

