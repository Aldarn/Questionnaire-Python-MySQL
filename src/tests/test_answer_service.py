#!/usr/bin/python2.7

import unittest
import mock
from ..core.domain.answer import Answer
from ..core.services.answer_service import answerService

class TestAnswerService(unittest.TestCase):
	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = None))
	@mock.patch('src.core.db.DB.commit', mock.MagicMock(return_value = None))
	def testCreate(self):
		answer = Answer(1, 2, "F")
		# -------------------------------------------------------
		answerService.create(answer)
		# -------------------------------------------------------
		# There should be no change to the object...
		self.assertEqual(answer.questionId, 1)
		self.assertEqual(answer.sessionId, 2)
		self.assertEqual(answer.answer, "F")

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"question_id": 1, "session_id": 2, "answer": "F"},
		{"question_id": 2, "session_id": 3, "answer": "T"}]))
	def testGetSessionAnswers(self):
		sessionId = 1
		# -------------------------------------------------------
		answers = answerService.getSessionAnswers(sessionId)
		# -------------------------------------------------------
		self.assertEqual(len(answers), 2)

	def testMap(self):
		answerResult = {"question_id": 1, "session_id": 2, "answer": "F"}
		# -------------------------------------------------------
		answer = answerService._map(answerResult)
		# -------------------------------------------------------
		self.assertEquals(answer.questionId, answerResult["question_id"])
		self.assertEquals(answer.sessionId, answerResult["session_id"])
		self.assertEquals(answer.answer, answerResult["answer"])

def main():
	unittest.main()

if __name__ == '__main__':
	main()
