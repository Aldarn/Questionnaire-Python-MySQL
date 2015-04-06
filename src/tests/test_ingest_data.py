#!/usr/bin/python2.7

import os
import unittest
from ..core import db
from ..core.common import isEligible
from ..scripts.ingest_data import main as ingestDataMain
from ..core.services.patient_service import patientService
from ..core.services.session_service import sessionService
from ..core.services.answer_service import answerService

class TestIngestData(unittest.TestCase):
	def setUp(self):
		# Modify the db handle to point to the test database
		db.db = db.DB("questionnaire_test")

		# Empty the database to begin with (except questions since they're not modified)
		db.db.query("SET FOREIGN_KEY_CHECKS = 0; TRUNCATE TABLE answers; TRUNCATE TABLE sessions; "
			"TRUNCATE TABLE patients; SET FOREIGN_KEY_CHECKS = 1;")

	def tearDown(self):
		db.db.close()

	def testIngestDataMain(self):
		dataFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/test_data.csv")
		# -------------------------------------------------------
		ingestDataMain(dataFile)
		# -------------------------------------------------------
		# Check all patients were created
		patients = patientService.getAll()
		self.assertEqual(len(patients), 4)

		# Check each patient has a session
		for patient in patients:
			sessions = sessionService.getPatientSessions(patient.id)
			self.assertEqual(len(sessions), 1)

			# Check each session has 5 acceptable answers
			for session in sessions:
				answers = answerService.getSessionAnswers(session.id)
				self.assertEqual(len(answers), 5)
				for answer in answers:
					self.assertIn(answer.answer, ['T', 'F', 'U'])

				# Check the eligibility was correctly set
				self.assertEqual(session.eligible, isEligible(answers))

def main():
	unittest.main()

if __name__ == '__main__':
	main()
