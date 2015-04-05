import MySQLdb

class DB(object):
	def __init__(self):
		self._connect()

	def _connect(self):
		"""
		Connects to the MySQL database and creates a cursor.

		TODO: Should probably be using this within a with() to automatically
		close the cursor after use. Should also use connection pooling.
		"""
		self.db = MySQLdb.connect(
			host="localhost",
			user="fake",
			passwd="fake",
			db="questionnaire"
		)
		self.dbHandle = self.db.cursor()

	def query(self):
		pass

	def close(self):
		self.db.close()
		self.dbHandle.close()

db = DB()
