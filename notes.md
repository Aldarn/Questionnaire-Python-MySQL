Overview of Solution
--------------------

TODO

I decided to record the unanswered questions (`U's`) in the database as well as the yesses (`T's`) and nos (`F's`). It 
could be argued that unanswered questions could simply have omitted rows in the answers table thus saving some disk 
space. I opted against this for ease of querying and completion of the data set, although i'm not sure it matters much 
either way.

An argument could be made for using mocking to test the various database methods instead of creating a test database 
and actually performing IO operations. One could also argue that it would be good to have both. Personally I prefer 
integration tests for this kind of operation for the additional solidarity that it's going to behave exactly as you 
expect both when entering the data and retrieving it later on. The downside is of course the extra effort in writing the 
tests, setting up and tearing down the test database and the additional time taken for these tests to run.

* Discuss complexity of queries
* getEligibleCount become obsolete when getEligibleChance was modified to also return total eligible count
* Discuss getEligibleChance, possibly paste the method description in here and also refer to the code?

What I Would Change With More Time
----------------------------------

TODO

* UI instead of command line
* Better handling of the DB with connection pools, transactions and so forth
* Some kind of clever way of predicting the values of unknowns
	* Looking at the %age yes for each question and factoring that in for the unknown value?
	* Asking additional questions that could determine the answer to the original question 
	* Using answers to other questions to gauge the chance of the unknown being true or false e.g. smokers more likely 
	to have high blood pressure
* Investigate generifying the services a bit more (seems to be a fair amount of overlap)
* E-mails or passwords for patients
* Simplified queries, using views, etc
* Services should actually be DAO's
* All business logic in services (non query methods) should stay in services
* Interfaces between services and daos for database agnostic code + same with services

As mentioned in the overview of the solution, testing database methods requires a separate test database to be 
pre-configured. This should be done a bit smarter either by using an existing library or framework to take care of it 
or at least creating and destroying the database at the start and end of testing. 

Limitations
-----------

I had to convert the given csv data file into unix format from Windows as the Python CSV library was not playing nicely 
with Windows line endings on my Mac; I tried using an answer from StackOverflow[0] to fix this however that resulted in 
the values not being separated at all (basically the CSV library doing nothing!).
	
Patients do not enter any kind of uniquely identifiable information e.g. an e-mail or password. This means that when 
a patient reuses the system they could enter any name of a previous patient and assume their identity. It also means 
patients with the same name would end up sharing session histories. 

	[0] http://stackoverflow.com/questions/17315635/csv-new-line-character-seen-in-unquoted-field-error

getEligibleCount Benchmarking
-----------------------------

The getEligibleCount query was a particularly interesting exercise to explore with several possible solutions and no 
clear winner even with SQL EXPLAIN and SQL_NO_CACHE to prevent cached results altering the benchmarking. 

Below is a list of the different queries tried that return the correct result, with their average query speed against 
a collection of 102 sessions for reference:

1. Using SUM and a LEFT JOIN trick with no WHERE clause on eligibility (`~1.5ms average`):

		SELECT SQL_NO_CACHE SUM(sessions1.eligible) AS eligibleCount 
		FROM sessions AS sessions1 
		LEFT JOIN sessions AS sessions2 
		ON sessions1.patient_id = sessions2.patient_id 
		AND sessions1.created < sessions2.created 
		WHERE sessions2.patient_id IS NULL

2. Using a subquery within the WHERE clause (`~1ms average`):

		SELECT SQL_NO_CACHE COUNT(sessions1.id) AS eligibleCount 
		FROM sessions sessions1
		WHERE sessions1.eligible = 1 
		AND sessions1.created = (
			SELECT MAX(sessions2.created) 
			FROM sessions sessions2 
			WHERE sessions1.patient_id = sessions2.patient_id 
			AND sessions1.eligible = 1
		)

3. Using COUNT and a LEFT JOIN trick with a WHERE clause on eligibility (`~0.7ms average`):

		SELECT SQL_NO_CACHE COUNT(sessions1.id) AS eligibleCount 
		FROM sessions AS sessions1 
		LEFT JOIN sessions AS sessions2 
		ON sessions1.patient_id = sessions2.patient_id 
		AND sessions1.created < sessions2.created 
		WHERE sessions2.patient_id IS NULL 
		AND sessions1.eligible = 1

4. Using a subquery within an INNER JOIN (`~1.75ms average`):

		SELECT SQL_NO_CACHE COUNT(sessions1.id) AS eligibleCount 
		FROM sessions sessions1 
		INNER JOIN(
			SELECT patient_id, MAX(created) maxCreated
			FROM sessions
			GROUP BY patient_id
		) sessions2 
		ON sessions1.patient_id = sessions2.patient_id 
		AND sessions1.created = sessions2.maxCreated 
		AND sessions1.eligible = 1

TODO List
---------

* Create setup.py
* Create interactive mode
* Create questionnaire mode
* Create get matches query