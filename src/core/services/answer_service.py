from service import Service

class AnswerService(Service):
	def __init__(self):
		super(AnswerService, self).__init__()

	def create(self, answer):
		"""
		Inserts the given answer into the database.

		:param answer: Answer object to insert.
		"""
		self.db.query("INERT INTO answers (question_id, session_id, answer) VALUES (%s, %s, %s)",
			(answer.questionId, answer.sessionId, answer.answer))
		self.db.commit()

answerService = AnswerService()