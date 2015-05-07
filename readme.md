Introduction
------------

Please follow the instructions in this readme in order to install and run the questionnaire. Additional notes can be 
found in the notes.md file.

These files are written using Markdown; viewing them within the Bitbucket repository or another markdown parser will 
render them in a simple wiki style format. They should however also be perfectly readable as plain text.

Installation
============

The following binaries need installing:

* Python 2.7
* MySQL 5.6.23 (Although 5+ should work)

The project can then be installed using the setup script:

	./setup.py install
	
Alternatively the project can be setup by extracting the source code somewhere convenient. The following additional 
python libraries must then also be installed:

* MySQLdb

		pip install MySQL-python

* Faker 
		
		pip install fake-factory

* mock 
		
		pip install mock
		
This has only been tested on unix-like systems, your mileage may vary with Windows (or other unix distros!).

Running the Questionnaire
=========================

1. Ensure MySQL is installed and running. 
2. Create two databases, `questionnaire` and `questionnaire_test`.
3. Run the SQL file in the sql directory against both databases to create the initial table structure.
4. Update the `_connect` method in `src/core/db.py` to use your MySQL credentials.
5. Populate the database using the ingest data script by running the following from a command line interface:

		./src/scripts/ingest_data.py
6. Execute the following from a command line interface from the project base directory:

		./src/launch_questionnaire.py

Tests
=====

To run all the tests, execute the following from a command line interface when the
current directory is the same as the one this file is in:

	python -m unittest discover

Alternatively run `nosetests` if you have nose installed.