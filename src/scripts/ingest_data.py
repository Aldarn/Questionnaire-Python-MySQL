#!/usr/bin/python2.7

import os
import csv

from faker import Faker
from src.core.common import isEligible

from src.core.domain.answer import Answer
from src.core.domain.patient import Patient
from src.core.domain.session import Session

from src.core.services.answer_service import answerService
from src.core.services.patient_service import patientService
from src.core.services.session_service import sessionService
from src.core.services.question_service import questionService

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
	main(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/trialsurveyunix.csv"))
