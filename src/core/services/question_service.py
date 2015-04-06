from service import Service

class QuestionService(Service):
	def __init__(self):
		super(QuestionService, self).__init__()

	def create(self, obj):
		pass

questionService = QuestionService()
