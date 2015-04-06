#!/usr/bin/python2.7

import csv

from faker import Faker
from ..core.common import isEligible

from ..core.domain.answer import Answer
from ..core.domain.patient import Patient
from ..core.domain.session import Session

from ..core.services.answer_service import answerService
from ..core.services.patient_service import patientService
from ..core.services.session_service import sessionService

def main(dataFile):
	faker = Faker()

	with open(dataFile, 'r') as fileHandle:
		for entry in csv.reader(fileHandle):
			# Create a patient entry
			patient = patientService.save(Patient(faker.name()))

			# Create a session entry
			session = sessionService.save(Session(patient.id))

			# Create the answers
			answers = []
			for questionId, rawAnswer in enumerate(entry):
				# TODO: Relying on the enumeration as the questionId is brittle since
				# the auto_increment doesn't necessarily start at 1 - improve this
				# by getting the actual id's for each question from the database
				answer = Answer(questionId + 1, session.id, rawAnswer)
				answerService.save(answer)
				answers.append(answer)

			# Save the eligibility
			sessionService.updateEligibility(session, isEligible(answers))

if __name__ == '__main__':
	main("../../../data/trialsurvey.csv")
