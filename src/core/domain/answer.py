from db_object import DBObject

class Answer(DBObject):
	def __init__(self, questionId, sessionId, answer):
		self._questionId = questionId
		self._sessionId = sessionId
		self._answer = answer

	@property
	def questionId(self):
		return self._questionId

	@property
	def sessionId(self):
		return self._sessionId

	@property
	def answer(self):
		return self._answer

	def __str__(self):
		return "session %i question %i answer %r" % (self.questionId, self.sessionId, self.answer)

	def __repr__(self):
		return "Answer(%i, %i, %r)" % (self.questionId, self.sessionId, self.answer)
