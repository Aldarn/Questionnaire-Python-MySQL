#!/usr/bin/python2.7

import unittest
import mock

from ..core.domain.question import Question
from ..core.services.question_service import questionService

class TestQuestionService(unittest.TestCase):
	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"question": "Singleton = evil -> GoF = evil?", "id": 1}]))
	def testGet(self):
		id = 1
		# -------------------------------------------------------
		question = questionService.get(id)
		# -------------------------------------------------------
		self.assertEqual(question.id, id)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"question": "Ruby on wheels?", "id": 1},
	   {"question": "Or Ruby on whales?", "id": 2}]))
	def testGetAll(self):
		# -------------------------------------------------------
		questions = questionService.getAll()
		# -------------------------------------------------------
		self.assertEqual(len(questions), 2)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = None))
	@mock.patch('src.core.db.DB.commit', mock.MagicMock(return_value = None))
	@mock.patch.object(questionService, 'get', mock.MagicMock(return_value = Question("Tabs or spaces?", 1)))
	def testCreate(self):
		question = Question("Tabs or spaces?")
		# -------------------------------------------------------
		questionResult = questionService.create(question)
		# -------------------------------------------------------
		self.assertEqual(questionResult.question, "Tabs or spaces?")
		self.assertEqual(questionResult.id, 1)

	def testMap(self):
		questionResult = {"question": "Camel case or underscores?", "id": 1}
		# -------------------------------------------------------
		question = questionService._map(questionResult)
		# -------------------------------------------------------
		self.assertEqual(question.question, "Camel case or underscores?")
		self.assertEqual(question.id, 1)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
