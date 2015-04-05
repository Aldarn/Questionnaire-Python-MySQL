from service import Service

class PatientService(Service):
	def __init__(self):
		super(PatientService, self).__init__()

	def create(self, obj):
		pass

patientService = PatientService()