from db_object import DBObject

class Patient(DBObject):
	def __init__(self, name, id = None, joined = None):
		self._name = name
		self._id = id
		self._joined = joined

	@property
	def id(self):
		return self._id

	@property
	def joined(self):
		return self._joined

	@property
	def name(self):
		return self.name

	def __str__(self):
		return "%s (joined %s)" % (self.name, self.joined)

	def __repr__(self):
		return "Patient(%i, %s, %s)" % (self.id, self.name, self.joined)
