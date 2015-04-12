import re

from service import Service, NoResultFound
from ..domain.patient import Patient
from ..common import getUserInput

class PatientService(Service):
	def __init__(self):
		super(PatientService, self).__init__()

	def get(self, id):
		"""
		Gets a patient object from the database by the given id.

		:param id: The id of the patient object to get.
		:return:
		"""
		try:
			patientResult = Service.db.query("SELECT * FROM patients WHERE id = %s", id)[0]
			return self._map(patientResult)
		except IndexError, e:
			raise NoResultFound("No patient was found with id %i" % id)

	def getByName(self, name):
		"""
		Gets a patient object from the database by the given name.

		:param name: The name of the patient object to get.
		:return:
		"""
		try:
			patientResult = Service.db.query("SELECT * FROM patients WHERE name = %s", name)[0]
			return self._map(patientResult)
		except IndexError, e:
			raise NoResultFound("No patient was found with name %s" % name)

	def getAll(self):
		"""
		Gets all patient objects from the database.

		:return: List of patient objects.
		"""
		patientResults = Service.db.query("SELECT * FROM patients")
		return [self._map(patientResult) for patientResult in patientResults]

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
		return int(eligibleCount[0]["eligibleCount"])

	def getEligibleChance(self, sessionId, answers):
		"""
		Calculates the eligibility chance based on the number of currently eligible patients and the number of patients'
		latest sessions that have answers matching the given list of answers.

		The matching works by grouping all answers by session and combining them into a string, thus getting one row of all
		answers for each session. We create a similar matcher string by combining the list of answers given, replacing
		unknown answers with wildcards representing "1 of any answer" and trailing wildcards with a suffix wildcard
		representing "0 or more of any answer". The set of all grouped answers is then filtered by removing the current
		session, removing sessions that are not the latest for their corresponding patients and by the matcher string.
		This set represents all previous patients that had the same (or possibly the same when considering unknown answers)
		answers as given in the provided session.

		For example:
			- Current answers: FUF
			- Matcher string: F_F%
			- Previous sessions answers: FFFFF, FUFTF, TTTTT, UUUFT, FTF
			- Matches: FFFFF, FUFTF, FTF

		The purpose of the suffix wildcard replacing the previous wildcards is to allow for partial sessions to be
		included in the set of possible matches, for example:
			- Matcher string without suffix wildcard: F_F__
			- Previous session answer: FUF
			- Result: No match since F_F___ is looking for answer strings of length 5

			- Matcher string with suffix wildcard: F_F%
			- Previous session answer: FUF
			- Result: Match since FUF == F[any]F[0 or more of any]

		Finally to calculate the eligibility chance we simply select the number of eligible patients from the matched
		set and divide that by the total number of matched patients.

		:param sessionId: The session id the given answers belong to, so we can omit it from the results.
		:param answers: The current answers to match against.
		:return: The chance this session will be eligible as a percentage.
		"""
		# Concatenate all answers
		answersString = "".join([answer.answer for answer in answers])

		# If they answered true to any question they are not eligible
		if 'T' in answersString:
			return 0

		# Get a matching string including wildcards (1 of any answer) for unknowns for the SQL query
		answersString = answersString.replace('U', '_')

		# Remove trailing wildcards and replace with % (0 or more of any answer) to include incomplete sessions if
		# applicable
		answersString = re.sub(r'(^.*?[F]*)(_*)$', r'\1%', answersString)

		# Run the query to calculate the eligibility chance
		eligibleChance = Service.db.query(
			"SELECT FLOOR((SUM(CASE WHEN matches.eligible = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100) AS eligibleChance "
			"FROM ("
			"	SELECT sessions1.id, sessions1.eligible "
			"	FROM questions "
			"	LEFT JOIN answers "
			"	ON answers.question_id = questions.id "
			"	LEFT JOIN sessions AS sessions1 "
			"	ON sessions1.id = answers.session_id "
			"	LEFT JOIN sessions AS sessions2 "
			"	ON sessions1.patient_id = sessions2.patient_id "
			"	AND sessions1.created < sessions2.created "
			"	WHERE sessions2.patient_id IS NULL "
			"	AND answers.session_id != %s "
			"	GROUP BY answers.session_id "
			"	HAVING GROUP_CONCAT(answers.answer ORDER BY questions.id ASC SEPARATOR '') LIKE %s"
			") matches",
			sessionId, answersString
		)[0]["eligibleChance"]

		# Return the chance or 1 if the chance is 0 since there is always hope (i.e. the chance was so small it was < 1
		# or there are currently no eligible patients in the system) :)
		return int(eligibleChance) if eligibleChance is not None and int(eligibleChance) > 0 else 1

	def createOrGetFromInput(self):
		"""
		Asks the patient for their name and either retrieves an existing patient record if they are already registered
		or creates a new one.

		:return: The new patient object.
		"""
		# Get the name
		patientName = getUserInput("What is your name? ")

		try:
			# Try and find an already registered patient
			return self.getByName(patientName)
		except NoResultFound:
			# This patient doesn't exist so create a new one
			return self.create(Patient(patientName))

	def _map(self, patientResult):
		return Patient(patientResult["name"], int(patientResult["id"]), patientResult["joined"])

patientService = PatientService()