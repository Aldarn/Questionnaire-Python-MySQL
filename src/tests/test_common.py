#!/usr/bin/python2.7

import unittest
import common
from ..core.common import *
from ..core.domain.answer import Answer
from ..core.services.answer_service import AnswerService

class TestCommon(unittest.TestCase):
	def testGetUserInput(self):
		prompt = "test"
		inputFunction = lambda s: "userInput"
		# -------------------------------------------------------
		result = getUserInput(prompt, inputFunction = inputFunction)
		# -------------------------------------------------------
		self.assertEqual(result, "userInput")

	def testGetUserInputType(self):
		prompt = "test"
		userInput = "7"
		inputFunction = lambda s: userInput
		# -------------------------------------------------------
		result = getUserInput(prompt, returnType = int, inputFunction = inputFunction)
		# -------------------------------------------------------
		self.assertEqual(result, int(userInput))
		self.assertTrue(isinstance(result, int))

	def testGetUserInputWithValidOption(self):
		self._getUserInputWithOptionsTest(lambda s: 'y')

	def testGetUserInputWithInvalidOption(self):
		self._getUserInputWithOptionsTest(self._optionsInvalidInputFunction)

	def _getUserInputWithOptionsTest(self, inputFunction):
		prompt = "yes or no?"
		options = {'y', 'n', 's'}
		# -------------------------------------------------------
		result = getUserInput(prompt, options = options, inputFunction = inputFunction)
		# -------------------------------------------------------
		self.assertEqual(result, 'y')

	def _optionsInvalidInputFunction(self, prompt, _hasPrompted = [False]):
		if not _hasPrompted[0]:
			_hasPrompted[0] = True
			return ""
		else:
			return 'y'

	def testIsEligibleIsEligible(self):
		# -------------------------------------------------------
		eligible = isEligible(common.getTestAnswers(possibleAnswers = 'F'))
		# -------------------------------------------------------
		self.assertTrue(eligible)

	def testIsEligibleNotEligible(self):
		# -------------------------------------------------------
		eligible = isEligible(common.getTestAnswers())
		# -------------------------------------------------------
		self.assertFalse(eligible)

	def testIsEligibleInsufficientAnswers(self):
		# -------------------------------------------------------
		eligible = isEligible(common.getTestAnswers(total = 4))
		# -------------------------------------------------------
		self.assertFalse(eligible)

def main():
	unittest.main()

if __name__ == '__main__':
	main()