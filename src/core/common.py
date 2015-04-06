def getUserInput(prompt, options = None, returnType = str, inputFunction = raw_input):
	"""
	Prompts the user for input and returns the result.

	:param prompt: The prompt to display.
	:param options: Optional options the user must choose from, defaults to none.
	:param returnType: Option return type, defaults to string.
	:param inputFunction: The function to use to receive the user input, defaults to raw_input.
	:return: The result casted to the given return type.
	"""
	optionString = " (%s)" % ", ".join(options) if options is not None else ""
	userInput = inputFunction("%s%s" % (prompt, optionString))
	if options is not None:
		if userInput not in options:
			print "\nPlease choose one from the following options:\n\n%s\n" % "\n".join(options)
			userInput = getUserInput(prompt, options, returnType, inputFunction)
	return returnType(userInput)

def isEligible(answers):
	"""
	Determines if the patient is eligible for trial based on the given answers.

	:param answers: Answer objects to check for eligibility.
	:return: True of eligible or false otherwise.
	"""
	if len(answers) < 5:
		return False

	for answer in answers:
		if answer.answer == 'T' or answer.answer == 'U':
			return False
	return True
