from ..core.domain.answer import Answer

def getTestAnswers(possibleAnswers = ('T', 'F', 'U')):
	return [Answer(i, i, possibleAnswers[i % len(possibleAnswers)]) for i in range(0, 5)]
