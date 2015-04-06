from db_object import DBObject

class Session(DBObject):
	def __init__(self, patient_id, id = None, created = None, eligible = False):
		self._patientId = patient_id
		self._id = id
		self._created = created
		self._eligible = eligible

	@property
	def id(self):
		return self._id

	@property
	def patientId(self):
		return self._patientId

	@property
	def created(self):
		return self._created

	@property
	def eligible(self):
		return self._eligible

	@eligible.setter
	def eligible(self, eligible):
		self._eligible = eligible

	def __str__(self):
		return "%i %s" % (self.patientId, self.created)

	def __repr__(self):
		return "Session(%i, %i, %s, %r)" % (self.id, self.patientId, self.created, self.eligible)
