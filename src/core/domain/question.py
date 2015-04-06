from db_object import DBObject

class Question(DBObject):
	def __init__(self, question, id = None):
		self._id = id
		self._question = question

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
		self._id = id

	@property
	def question(self):
		return self._question

	def __str__(self):
		return self.question

	def __repr__(self):
		return "Question(%i, %s)" % (self.id, self.question)
