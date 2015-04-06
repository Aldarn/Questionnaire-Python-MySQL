#!/usr/bin/python2.7

import unittest
from ..core import db
from ..scripts.ingest_data import main as ingestDataMain
from ..core.services.patient_service import patientService
from ..core.services.session_service import sessionService
from ..core.services.answer_service import answerService

class TestIngestData(unittest.TestCase):
	def setUp(self):
		# Modify the db handle to point to the test database
		db.db = db.DB("questionnaire_test")

		# Empty the database to begin with (except questions since they're not modified)
		# TODO: Just doing patients should cascade foreign keys?
		db.db.query("TRUNCATE TABLE answers; TRUNCATE TABLE patients; TRUNCATE TABLE sessions;")

	def tearDown(self):
		db.db.close()

	def testIngestDataMain(self):
		dataFile = "../../../data/test_data.csv"
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

def main():
	unittest.main()

if __name__ == '__main__':
	main()
