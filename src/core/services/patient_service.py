from service import Service
from ..domain.patient import Patient

class PatientService(Service):
	def __init__(self):
		super(PatientService, self).__init__()

	def get(self, id):
		patientResult = self.db.query("SELECT * FROM patients WHERE id = %s", id)
		return Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"])

	def getAll(self):
		patientsResult = self.db.query("SELECT * FROM patients")
		return [Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"]) for patientResult in patientsResult]

	def create(self, patient):
		"""
		Inserts the given patient into the database.

		:param patient: Patient object to insert.
		:return: Newly inserted patient object.
		"""
		self.db.query("INERT INTO patients (id, name, joined) VALUES ('', %s, '')", patient.name)
		self.db.commit()

		# Reload the object to ensure auto rows are filled
		return self.get(self.db.lastRowId())

patientService = PatientService()