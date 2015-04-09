from services.patient_service import patientService
from services.session_service import sessionService
from services.question_service import questionService
from services.answer_service import answerService

from domain.session import Session
from domain.answer import Answer

from common import getUserInput, isEligible

class Questionnaire(object):
	def __init__(self):
		pass

	def run(self):
		"""
		Runs the questionnaire.
		"""
		print "Welcome to the questionnaire! Please answer all questions honestly; if you do not know any answers then " \
			  "please skip the question. Good luck!\n"

		# Get the patient
		patient = patientService.createOrGetFromInput()

		# Create a new session
		session = sessionService.create(Session(patient.id))

		# Get all the questions
		questions = questionService.getAll()

		# Ask each question and record the answers
		answers = []
		for question in questions:
			print "Your current eligibility chance is %i%%\n" % patientService.getEligibleChance(session.id, answers)

			# TODO: Encapsulate this in the question service, use user friendly names and map the results
			answer = getUserInput("%s  " % question.question, ["T", "F", "U"])

			# Save the answer
			answer = Answer(question.id, session.id, answer)
			answerService.create(answer)
			answers.append(answer)

		print "\nThank you for finishing the questionnaire!"

		print "Congratulations, you are eligible for the trial!" if isEligible(answers) else "Unfortunately you are " \
		 	"not eligible for this clinical trial; if your circumstances chance please revisit us. We wish you the best" \
			"of health :)"