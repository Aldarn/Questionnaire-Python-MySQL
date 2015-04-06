from service import Service
from ..domain.question import Question

class QuestionService(Service):
	def __init__(self):
		super(QuestionService, self).__init__()

	def get(self, id):
		questionResult = self.db.query("SELECT * FROM questions WHERE id = %i", id)
		return Question(questionResult["question"], int(questionResult["id"]))

	def getAll(self):
		questionResults = self.db.query("SELECT * FROM questions")
		return [Question(questionResult["question"], int(questionResult["id"])) for questionResult in questionResults]

	def create(self, question):
		"""
		Inserts the given question into the database.

		:param question: Question object to insert.
		:return: Inserted question object.
		"""
		self.db.query("INERT INTO questions (id, question) VALUES ('', %s)", question.question)
		self.db.commit()

		question.id = self.db.lastRowId()
		return question

questionService = QuestionService()
