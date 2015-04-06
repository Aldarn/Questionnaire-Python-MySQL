from db_object import DBObject

class Session(DBObject):
	def __init__(self, patient_id, id = None, created = None):
		self._patientId = patient_id
		self._id = id
		self._created = created

	@property
	def id(self):
		return self._id

	@property
	def patientId(self):
		return self._patientId

	@property
	def created(self):
		return self._created

	def __str__(self):
		return "%i %s" % (self.patientId, self.created)

	def __repr__(self):
		return "Session(%i, %i, %s)" % (self.id, self.patientId, self.created)
