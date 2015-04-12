#!/usr/bin/python2.7

import unittest
import mock

from ..core.domain.session import Session
from ..core.services.session_service import sessionService

class TestSessionService(unittest.TestCase):
	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"patient_id": 1, "id": 2, "created": "whenever", "eligible": False}]))
	def testGet(self):
		id = 2
		# -------------------------------------------------------
		session = sessionService.get(id)
		# -------------------------------------------------------
		self.assertEqual(session.id, id)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"patient_id": 1, "id": 2, "created": "whenever", "eligible": False},
	   {"patient_id": 1, "id": 3, "created": "whenever", "eligible": False}]))
	def testGetAll(self):
		# -------------------------------------------------------
		sessions = sessionService.getPatientSessions(1)
		# -------------------------------------------------------
		self.assertEqual(len(sessions), 2)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = None))
	@mock.patch('src.core.db.DB.commit', mock.MagicMock(return_value = None))
	@mock.patch.object(sessionService, 'get', mock.MagicMock(return_value = Session(1, 2, "whenever", True)))
	def testCreate(self):
		session = Session(1)
		# -------------------------------------------------------
		sessionResult = sessionService.create(session)
		# -------------------------------------------------------
		self.assertEqual(sessionResult.patientId, 1)
		self.assertEqual(sessionResult.id, 2)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = None))
	@mock.patch('src.core.db.DB.commit', mock.MagicMock(return_value = None))
	def testUpdateEligibility(self):
		session = Session(1, 2, "whenever", True)
		# -------------------------------------------------------
		sessionResult = sessionService.updateEligibility(session, False)
		# -------------------------------------------------------
		self.assertEqual(sessionResult.eligible, False)

	def testMap(self):
		sessionResult = {"patient_id": 1, "id": 2, "created": "whenever", "eligible": False}
		# -------------------------------------------------------
		session = sessionService._map(sessionResult)
		# -------------------------------------------------------
		self.assertEqual(session.patientId, 1)
		self.assertEqual(session.id, 2)
		self.assertEqual(session.created, "whenever")
		self.assertEqual(session.eligible, False)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
