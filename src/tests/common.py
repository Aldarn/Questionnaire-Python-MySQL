from ..core.domain.answer import Answer
from ..core.services.answer_service import AnswerService

def getTestAnswers(possibleAnswers = AnswerService.ACCEPTABLE_ANSWERS.values(), total = 5):
	return [Answer(i, i, possibleAnswers[i % len(possibleAnswers)]) for i in range(0, total)]
