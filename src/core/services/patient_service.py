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
		patientResult = Service.db.query("SELECT * FROM patients WHERE id = %s", id)[0]
		return Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"])

	def getAll(self):
		"""
		Gets all patient objects from the database.

		:return: List of patient objects.
		"""
		patientResults = Service.db.query("SELECT * FROM patients")
		return [Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"]) for patientResult in patientResults]

	def create(self, patient):
		"""
		Inserts the given patient into the database.

		:param patient: Patient object to insert.
		:return: Newly inserted patient object.
		"""
		if patient.id is not None:
			raise ValueError("Tried to create an already existent patient (%s)." % patient)

		Service.db.query("INSERT INTO patients (name) VALUES (%s)", patient.name)
		Service.db.commit()

		# Reload the object to ensure auto rows are filled
		return self.get(Service.db.lastRowId())

	def getEligibleCount(self):
		"""
		Gets the total number of currently eligible patients (as of the last time they took the questionnaire). This
		query takes into account the fact that the patient may have taken the questionnaire several times, with the
		latest being the result that matters.

		I benchmarked this query against several other versions with this version being the most efficient on average.
		Please refer to the notes to see the other variations.

		:return: The number of eligible patients.
		"""
		eligibleCount = Service.db.query(
			"SELECT COUNT(sessions1.id) AS eligibleCount "
			"FROM sessions AS sessions1 "
			"LEFT JOIN sessions AS sessions2 "
			"ON sessions1.patient_id = sessions2.patient_id "
			"AND sessions1.created < sessions2.created "
			"WHERE sessions2.patient_id IS NULL "
			"AND sessions1.eligible = 1"
		)
		return int(eligibleCount["count"])

patientService = PatientService()