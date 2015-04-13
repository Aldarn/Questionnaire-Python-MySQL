#!/usr/bin/python2.7

import unittest
import mock

from ..core.questionnaire import Questionnaire
from ..core.domain.patient import Patient
from ..core.domain.question import Question
from ..core.domain.session import Session

from ..core.services.answer_service import answerService
from ..core.services.patient_service import patientService
from ..core.services.question_service import questionService
from ..core.services.session_service import sessionService

class TestQuestionnaire(unittest.TestCase):
	@mock.patch.object(patientService, 'getEligibleCount', mock.MagicMock(return_value = 10))
	@mock.patch.object(patientService, 'createOrGetFromInput', mock.MagicMock(return_value = Patient("Test", 1, "joined")))
	@mock.patch.object(sessionService, 'getPatientSessions', mock.MagicMock(return_value = [1,2,3]))
	@mock.patch.object(sessionService, 'create', mock.MagicMock(return_value = Session(1, 1, "created", False)))
	@mock.patch.object(questionService, 'getAll', mock.MagicMock(return_value = [Question("Tabs or spaces?", 1)]))
	@mock.patch.object(patientService, 'getEligibleChance', mock.MagicMock(return_value = 10))
	@mock.patch.object(answerService, 'getFriendlyAnswers', mock.MagicMock(return_value = ["Yes", "No"]))
	@mock.patch.object(answerService, 'getAnswerFromFriendly', mock.MagicMock(return_value = "F"))
	@mock.patch.object(answerService, 'create', mock.MagicMock(return_value = None))
	@mock.patch('src.core.questionnaire.isEligible', mock.MagicMock(return_value = True))
	@mock.patch.object(sessionService, 'updateEligibility', mock.MagicMock(return_value = None))
	def testQuestionnaire(self):
		questionnaire = Questionnaire()
		# -------------------------------------------------------
		questionnaire.run()
		# -------------------------------------------------------
		# TODO: Test output

def main():
	unittest.main()

if __name__ == '__main__':
	main()
