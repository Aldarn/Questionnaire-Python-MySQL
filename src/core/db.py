import MySQLdb

class DB(object):
	"""
	Object encapsulating the database connection and operations.
	"""

	def __init__(self):
		self._connect()

	def _connect(self):
		"""
		Connects to the MySQL database and creates a cursor.

		TODO: Should probably be using this within a with() to automatically
		close the cursor after use. Should also use connection pooling.
		"""
		self._db = MySQLdb.connect(
			host = "localhost",
			user = "root",
			passwd = "",
			db = "questionnaire"
		)
		self._dbHandle = self.db.cursor()

	def query(self, query):
		"""
		Executes the given query and returns the results.

		:param query: The SQL to execute.
		:return: :ist of column:value dictionaries.
		"""
		self._dbHandle.execute(query)
		return self._dictFetchAll()

	def _dictFetchAll(self):
		"""
		Creates a dictionary of column:value from the results of a raw query.

		:return: Dictionary column:value.
		"""
		desc = self._dbHandle.description
		return [
			dict(zip([col[0] for col in desc], row))
			for row in self._dbHandle.fetchall()
		]

	def close(self):
		"""
		Closes the handle and connection.
		"""
		self._db.close()
		self._dbHandle.close()

db = DB()
