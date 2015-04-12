from service import Service
from ..domain.answer import Answer

class AnswerService(Service):

	ACCEPTABLE_ANSWERS = {"Yes": "T", "No": "F", "Skip": "U"}

	def __init__(self):
		super(AnswerService, self).__init__()

	def create(self, answer):
		"""
		Inserts the given answer into the database.

		:param answer: Answer object to insert.
		"""
		Service.db.query("INSERT INTO answers (question_id, session_id, answer) VALUES (%s, %s, %s)",
			answer.questionId, answer.sessionId, answer.answer)
		Service.db.commit()

	def getSessionAnswers(self, sessionId):
		"""
		Gets all answers for the given session id.

		:param sessionId: The session id to get the answers for.
		:return: List of session objects.
		"""
		answerResults = Service.db.query("SELECT * FROM answers WHERE session_id = %s", sessionId)
		return [self._map(answerResult) for answerResult in answerResults]

	def getFriendlyAnswers(self):
		"""
		Gets the answers that are displayed to the user as options when answering a question.

		:return: List of friendly answers.
		"""
		return AnswerService.ACCEPTABLE_ANSWERS.keys()

	def getAnswerFromFriendly(self, friendly):
		"""
		Gets the internal value of an answer from its user friendly name.

		:param friendly: The user friendly name.
		:return: The internal value.
		"""
		return AnswerService.ACCEPTABLE_ANSWERS[friendly]

	def _map(self, answerResult):
		return Answer(answerResult["question_id"], answerResult["session_id"], answerResult["answer"])

answerService = AnswerService()
