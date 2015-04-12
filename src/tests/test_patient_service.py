#!/usr/bin/python2.7

import unittest
import common
import mock
from ..core.services.patient_service import patientService

class TestPatientService(unittest.TestCase):
	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"eligibleChance": 50}]))
	def testGetEligibleChance(self):
		sessionId = 1
		answers = common.getTestAnswers(possibleAnswers = ('F', 'U'))
		# -------------------------------------------------------
		eligibleChance = patientService.getEligibleChance(sessionId, answers)
		# -------------------------------------------------------
		self.assertEqual(eligibleChance, 50)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"eligibleChance": 0}]))
	def testGetEligibleChanceNoCurrentEligiblePatients(self):
		sessionId = 1
		answers = common.getTestAnswers(possibleAnswers = ('F', 'U'))
		# -------------------------------------------------------
		eligibleChance = patientService.getEligibleChance(sessionId, answers)
		# -------------------------------------------------------
		self.assertEqual(eligibleChance, 1)

	def testGetEligibleChanceNotEligible(self):
		sessionId = 1
		answers = common.getTestAnswers()
		# -------------------------------------------------------
		eligibleChance = patientService.getEligibleChance(sessionId, answers)
		# -------------------------------------------------------
		self.assertEqual(eligibleChance, 0)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
