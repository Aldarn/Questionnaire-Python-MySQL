from service import Service
from ..domain.session import Session

class SessionService(Service):
	def __init__(self):
		super(SessionService, self).__init__()

	def get(self, id):
		"""
		Gets a session object with the given id from the database.

		:param id: The id of the session to get.
		:return: The loaded session object.
		"""
		sessionResult = Service.db.query("SELECT * FROM sessions WHERE id = %s", id)[0]
		return self._map(sessionResult)

	def getPatientSessions(self, patientId):
		"""
		Gets all sessions for the given patient id.

		:param patientId: The patient id to get the sessions for.
		:return: List of session objects.
		"""
		sessionResults = Service.db.query("SELECT * FROM sessions WHERE patient_id = %s", patientId)
		return [self._map(sessionResult) for sessionResult in sessionResults]

	def create(self, session):
		"""
		Inserts the given session into the database.

		:param session: Session object to insert.
		:return: Newly inserted session object.
		"""
		if session.id is not None:
			raise ValueError("Tried to create an already existent session (%s)." % session)

		Service.db.query("INSERT INTO sessions (patient_id, eligible) VALUES (%s, %s)",
			session.patientId, 1 if session.eligible else 0)
		Service.db.commit()

		# Reload the object to ensure auto rows are filled
		return self.get(Service.db.lastRowId())

	def updateEligibility(self, session, eligible):
		"""
		Updates the eligibility of an existing session.

		:param session: The session to update.
		:param eligible: If the session is eligible or not.
		:return: Updated session object.
		"""
		if session.id is None:
			raise ValueError("Tried to update the eligibility of a session that has not been saved in the database (%s)." % session)

		session.eligible = eligible
		Service.db.query("UPDATE sessions SET eligible = %s WHERE id = %s", 1 if eligible else 0, session.id)
		return session

	def _map(self, sessionResult):
		"""
		Maps a session database result to a session object.

		:param sessionResult: Session database result.
		:return: Session object.
		"""
		return Session(int(sessionResult["patient_id"]), int(sessionResult["id"]), sessionResult["created"],
			bool(sessionResult["eligible"]))

sessionService = SessionService()