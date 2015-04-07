Overview of Solution
--------------------

TODO

An argument could be made for using mocking to test the various database methods instead of creating a test database 
and actually performing IO operations. One could also argue that it would be good to have both. Personally I prefer 
integration tests for this kind of operation for the additional solidarity that it's going to behave exactly as you 
expect both when entering the data and retrieving it later on. The downside is of course the extra effort in writing the 
tests, setting up and tearing down the test database and the additional time taken for these tests to run.

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

As mentioned in the overview of the solution, testing database methods requires a separate test database to be 
pre-configured. This should be done a bit smarter either by using an existing library or framework to take care of it 
or at least creating and destroying the database at the start and end of testing. 

Limitations
-----------

I had to convert the given csv data file into unix format from Windows as the Python CSV library was not playing nicely 
with Windows line endings on my Mac; I tried using an answer from StackOverflow[0] to fix this however that resulted in 
the values not being separated at all (basically the CSV library doing nothing!).

	[0] http://stackoverflow.com/questions/17315635/csv-new-line-character-seen-in-unquoted-field-error
	
Patients do not enter any kind of uniquely identifiable information e.g. an e-mail or password. This means that when 
a patient reuses the system they could enter any name of a previous patient and assume their identity. It also means 
patients with the same name would end up sharing session histories. 

TODO List
---------

* Fix eligibility count query - http://stackoverflow.com/questions/537223/mysql-control-which-row-is-returned-by-a-group-by
* Create setup.py

SELECT SUM(sessions.eligible) as count 
FROM patients 
LEFT JOIN sessions 
ON sessions.patient_id = patients.id 
ORDER BY sessions.created DESC

SELECT *
FROM (
	SELECT id, max(version_id) as version_id 
	FROM table 
	GROUP BY id
) t1
INNER JOIN table t2 
on t2.id=t1.id 
and t1.version_id=t2.version_id