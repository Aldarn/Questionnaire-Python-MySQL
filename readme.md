Installation
============

The following binaries need installing:

* Python 2.7
* MySQL 5+
	
Along with the following additional python libraries:

* Faker - `pip install fake-factory`
* mock - `pip install mock`

Running the Questionnaire
=========================

1. Ensure MySQL is installed and running. 
2. Create two databases, `questionnaire` and `questionnaire_test`.
3. Run the SQL file in the sql directory against both databases to create the initial table structure.
4. Update the `_connect` method in `src/core/db.py` to use your MySQL credentials.
5. Execute the following from a command line interface from the project base directory:

		./launch.py

Tests
=====

To run all the tests, execute the following from a command line interface when the
current directory is the same as the one this file is in:

	python -m unittest discover

Alternatively run `nosetests` if you have nose installed.
