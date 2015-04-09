#!/usr/bin/python2.7

import argparse
from src.core.db import dbInstance
from src.core.questionnaire import Questionnaire

def getCommandLineArguments():
	"""
	Manages command line arguments and information.

	:return: Object containing arguments and values.
	"""
	# TODO: Finish this!
	parser = argparse.ArgumentParser(description="Clinical Trial Eligibility Questionnaire")
	return parser.parse_args()

def main():
	print "Welcome to the clinical trial eligibility questionnaire!\n"

	# Get any command line arguments supplied
	# TODO: Do something with these
	commandLineArguments = getCommandLineArguments()

	# Start the questionnaire
	Questionnaire().run()

	# Close the db connection
	# TODO: This should be used in a "with" statement along with connection pooling, but
	# that's out of the scope of this test
	dbInstance.close()

if __name__ == '__main__':
	main()
