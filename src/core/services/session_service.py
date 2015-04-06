from service import Service

class SessionService(Service):
	def __init__(self):
		super(SessionService, self).__init__()

	def create(self, obj):
		pass

	def updateEligibility(self, session, eligible):
		"""
		Updates the eligibility of an existing session.

		:param session: The session to update.
		:param eligible: If the session is eligible or not.
		:return: Updated session object.
		"""
		if session.id is None:
			raise ValueError("Tried to update the eligibility of a session that has not been saved in the database.")

		session.eligible = eligible
		self.db.query("UPDATE sessions SET eligible = %i WHERE id = %i", (1 if eligible else 0, session.id))
		return session

sessionService = SessionService()