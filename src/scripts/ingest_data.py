#!/usr/bin/python2.7

import csv
from ..core.domain.answer import Answer
from ..core.services.answer_service import answerService
from ..core.domain.patient import Patient
from ..core.services.patient_service import patientService
from ..core.domain.question import Question
from ..core.services.question_service import questionService
from ..core.domain.session import Session
from ..core.services.session_service import sessionService

def main(dataFile):
	with open(dataFile, 'r') as fileHandle:
		for entry in csv.reader(fileHandle):
			# Create a patient entry
			# TODO: Generate a name
			patient = Patient()
			patientService.save(patient)

			# Create a session entry
			session = Session(patient.id)
			sessionService.save(session)

			# Create the answers
			for questionId, rawAnswer in enumerate(entry):
				answer = Answer(questionId, session.id, True if rawAnswer is 'T' else False)
				answerService.save(answer)

if __name__ == '__main__':
	main("../../../data/trialsurvey.csv")
