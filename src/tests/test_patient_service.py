#!/usr/bin/python2.7

import unittest
import common
import mock

from ..core.domain.patient import Patient
from ..core.services.service import NoResultFound
from ..core.services.patient_service import patientService

class TestPatientService(unittest.TestCase):
	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"name": "patient", "id": 1, "joined": "whenever"}]))
	def testGet(self):
		id = 1
		# -------------------------------------------------------
		patient = patientService.get(id)
		# -------------------------------------------------------
		self.assertEqual(patient.id, id)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"name": "yuppity yup yup yup", "id": 1, "joined": "whenever"}]))
	def testGetByName(self):
		name = "yuppity yup yup yup"
		# -------------------------------------------------------
		patient = patientService.getByName(name)
		# -------------------------------------------------------
		self.assertEqual(patient.name, name)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"name": "patient", "id": 1, "joined": "whenever"},
		{"name": "patient2", "id": 2, "joined": "whenever2"}]))
	def testGetAll(self):
		# -------------------------------------------------------
		patients = patientService.getAll()
		# -------------------------------------------------------
		self.assertEqual(len(patients), 2)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = None))
	@mock.patch('src.core.db.DB.commit', mock.MagicMock(return_value = None))
	@mock.patch.object(patientService, 'get', mock.MagicMock(return_value = Patient("Bla Mcblarson", 1, "whatever")))
	def testCreate(self):
		patient = Patient("Bla Mcblarson")
		# -------------------------------------------------------
		patientResult = patientService.create(patient)
		# -------------------------------------------------------
		self.assertEqual(patientResult.name, "Bla Mcblarson")
		self.assertEqual(patientResult.id, 1)

	@mock.patch('src.core.db.DB.query', mock.MagicMock(return_value = [{"eligibleCount": 9001}]))
	def testGetEligibleCount(self):
		# -------------------------------------------------------
		eligibleCount = patientService.getEligibleCount()
		# -------------------------------------------------------
		self.assertEqual(eligibleCount, 9001)

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

	@mock.patch('src.core.services.patient_service.getUserInput', mock.MagicMock(return_value = "New Patient"))
	@mock.patch.object(patientService, 'getByName', mock.MagicMock(return_value = Patient("New Patient")))
	def testCreateOrGetFromInput(self):
		# -------------------------------------------------------
		patient = patientService.createOrGetFromInput()
		# -------------------------------------------------------
		self.assertEquals(patient.name, "New Patient")

	@mock.patch('src.core.services.patient_service.getUserInput', mock.MagicMock(return_value = "New Patient"))
	@mock.patch.object(patientService, 'getByName')
	@mock.patch.object(patientService, 'create', mock.MagicMock(return_value = Patient("New Patient")))
	def testCreateOrGetFromInputCreate(self, getByNameMock):
		patientName = "New Patient"
		getByNameMock.side_effect = NoResultFound()
		# -------------------------------------------------------
		patient = patientService.createOrGetFromInput()
		# -------------------------------------------------------
		self.assertRaises(NoResultFound, patientService.getByName, patientName)
		self.assertEquals(patient.name, patientName)

	def testMap(self):
		patientResult = {"name": "patient", "id": 1, "joined": "whenever"}
		# -------------------------------------------------------
		patient = patientService._map(patientResult)
		# -------------------------------------------------------
		self.assertEquals(patient.name, patientResult["name"])
		self.assertEquals(patient.id, patientResult["id"])
		self.assertEquals(patient.joined, patientResult["joined"])

def main():
	unittest.main()

if __name__ == '__main__':
	main()
