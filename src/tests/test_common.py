#!/usr/bin/python2.7

import unittest
from ..core.common import *

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
		self._getUserInputWithOptionsTest(self._optionsInputFunction)

	def _getUserInputWithOptionsTest(self, inputFunction):
		prompt = "yes or no?"
		options = ['y', 'n', 's']
		# -------------------------------------------------------
		result = getUserInput(prompt, options = options, inputFunction = inputFunction)
		# -------------------------------------------------------
		self.assertEqual(result, 'y')

	def _optionsInputFunction(self, prompt, _hasPrompted = [False]):
		if _hasPrompted[0]:
			_hasPrompted[0] = True
			return 'invalid'
		else:
			return 'y'

def main():
	unittest.main()

if __name__ == '__main__':
	main()