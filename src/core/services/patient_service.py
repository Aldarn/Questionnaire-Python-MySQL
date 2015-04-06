from service import Service
from ..domain.patient import Patient

class PatientService(Service):
	def __init__(self):
		super(PatientService, self).__init__()

	def get(self, id):
		"""
		Gets a patient object from the database by the given id.

		:param id: The id of the patient object to get.
		:return:
		"""
		patientResult = self.db.query("SELECT * FROM patients WHERE id = %s", id)[0]
		return Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"])

	def getAll(self):
		"""
		Gets all patient objects from the database.

		:return: List of patient objects.
		"""
		patientResults = self.db.query("SELECT * FROM patients")
		return [Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"]) for patientResult in patientResults]

	def create(self, patient):
		"""
		Inserts the given patient into the database.

		:param patient: Patient object to insert.
		:return: Newly inserted patient object.
		"""
		if patient.id is not None:
			raise ValueError("Tried to create an already existent patient (%s)." % patient)

		self.db.query("INSERT INTO patients (name) VALUES (%s)", patient.name)
		self.db.commit()

		# Reload the object to ensure auto rows are filled
		return self.get(self.db.lastRowId())

	def getEligibleCount(self):
		"""
		Gets the total number of currently eligible patients (as of the last time they took the questionnaire).

		:return: The number of eligible patients.
		"""
		eligibleCount = self.db.query(
			"SELECT COUNT(sessions.eligible) as count "
			"FROM patients "
			"LEFT JOIN sessions "
			"ON sessions.patient_id = patients.id "
			"GROUP BY patients.id "
			"ORDER BY sessions.created DESC"
		)
		return int(eligibleCount["count"])

patientService = PatientService()