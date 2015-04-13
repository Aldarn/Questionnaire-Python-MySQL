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
		print "Welcome to the questionnaire!\n" \
			  "There are currently %i eligible patients for this trial.\n" \
			  "Please answer all questions honestly; if you do not know any answers then " \
			  "please skip the question. Good luck!\n" % patientService.getEligibleCount()

		# Get the patient
		patient = patientService.createOrGetFromInput()

		# Indicate how many times they have done this before
		print "\nGood to see you, %s. You have completed this questionnaire %i times before." \
			  % (patient.name, len(sessionService.getPatientSessions(patient.id)))

		# Create a new session
		session = sessionService.create(Session(patient.id))

		# Get all the questions
		questions = questionService.getAll()

		# Ask each question and record the answers
		answers = []
		for question in questions:
			print "\nYour current eligibility chance is %i%%\n" % patientService.getEligibleChance(session.id, answers)

			answer = getUserInput("%s " % question.question, map(str.title, answerService.getFriendlyAnswers()))

			# Save the answer
			answer = Answer(question.id, session.id, answerService.getAnswerFromFriendly(answer))
			answerService.create(answer)
			answers.append(answer)

		print "\nThank you for finishing the questionnaire!"

		# Determine if they are eligible and update the session
		eligibility = isEligible(answers)
		sessionService.updateEligibility(session, eligibility)

		print "Congratulations, you are eligible for the trial!" if eligibility else "Unfortunately you are " \
		 	"not eligible for this clinical trial; if your circumstances chance please revisit us. We wish you the best" \
			"of health :)"