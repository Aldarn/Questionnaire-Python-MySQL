#!/usr/bin/python2.7

import os
import csv

from faker import Faker
from ..core.common import isEligible

from ..core.domain.answer import Answer
from ..core.domain.patient import Patient
from ..core.domain.session import Session

from ..core.services.answer_service import answerService
from ..core.services.patient_service import patientService
from ..core.services.session_service import sessionService
from ..core.services.question_service import questionService

def main(dataFile):
	faker = Faker()

	with open(dataFile, 'r') as fileHandle:
		for entry in csv.reader(fileHandle):
			# Skip header row
			if entry[0] == "pregnant":
				continue

			# Create a patient entry
			patient = patientService.create(Patient(faker.name()))

			# Create a session entry
			session = sessionService.create(Session(patient.id))

			# Load the questions
			questions = questionService.getAll()

			# Create the answers
			answers = []
			for i, rawAnswer in enumerate(entry):
				answer = Answer(questions[i].id, session.id, rawAnswer)
				answerService.create(answer)
				answers.append(answer)

			# Save the eligibility
			sessionService.updateEligibility(session, isEligible(answers))

if __name__ == '__main__':
	main(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/trialsurvey.csv"))
