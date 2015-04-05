from service import Service

class AnswerService(Service):
	def __init__(self):
		super(AnswerService, self).__init__()

	def create(self, obj):
		pass

answerService = AnswerService()