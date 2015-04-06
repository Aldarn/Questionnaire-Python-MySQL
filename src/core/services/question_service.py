from service import Service
from ..domain.question import Question

class QuestionService(Service):
	def __init__(self):
		super(QuestionService, self).__init__()

	def get(self, id):
		"""
		Gets a question object from the database by the given id.

		:param id: The id of the question to get.
		:return: Loaded question object.
		"""
		questionResult = self.db.query("SELECT * FROM questions WHERE id = %s", id)[0]
		return Question(questionResult["question"], int(questionResult["id"]))

	def getAll(self):
		"""
		Gets all question objects from the database.

		:return: List of loaded question objects.
		"""
		questionResults = self.db.query("SELECT * FROM questions ORDER BY id ASC")
		return [Question(questionResult["question"], int(questionResult["id"])) for questionResult in questionResults]

	def create(self, question):
		"""
		Inserts the given question into the database.

		:param question: Question object to insert.
		:return: Inserted question object.
		"""
		if question.id is not None:
			raise ValueError("Tried to create an already existent question (%s)." % question)

		self.db.query("INSERT INTO questions (question) VALUES (%s)", question.question)
		self.db.commit()

		question.id = self.db.lastRowId()
		return question

questionService = QuestionService()
