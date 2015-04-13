Overview of Solution
--------------------

In total I spent around 12 hours on this problem. This includes the initial planning stage of deciding how to approach 
the problem of calculating eligibility percentages whilst incorporating unknown values, researching existing solutions 
and creating a rough architecture on paper. I then setup the MySQL database, ensuring it was running correctly locally 
and designing the initial database structure. After that came the actual solution, which invariably involved small 
iterations on my original plan and database structure as problems became apparent during development. Finally this also 
includes the time spent to continuously record my readme instructions and notes and then finally write them up into 
a more formal document.

Overall there were three major decisions that led to this solution: the architecture of using a service and data 
oriented approach to separate control flow from business logic and data, using MySQL as a data store and the specific 
algorithm used to generate eligibility percentages. 

From experience I have found service oriented architecture tends to lead to fairly elegant solutions that ensure loose 
coupling and separation of concerns whilst also being simple to reason about. This makes decisions such as where to put 
specific pieces of functionality clearer for the programmer, tests are generally simpler to implement as the code is 
by nature more modular and if done correctly it should also be simple to completely change a services behaviour without 
affecting the underlying functionality that relies on the service.

The use of MySQL is debatable for this task; it would have been entirely feasible to simply use the data file as a 
single source of data by loading it into memory, performing calculations and writing fresh answers back to the file. 
If I had opted for this approach I would have saved a significant amount of time, for instance the ingest data script 
would not have been required to write to disk, there would have been no queries to write for retrieving or saving data 
and there would have been no setup for the database to begin with. However, there are many reasons that I decided to use 
MySQL. Firstly as a real world solution it would be unfeasible to use a flat file as it would be very inefficient, 
increasingly more so as the size of the data set increases to the point where it would be unusable. A flat file would 
also not support concurrency well, with a lack of a sophisticated locking system data would quickly become corrupted 
with various writes lost and overwritten. Secondly performing filtering and calculations on inherently relational data 
is a problem that naturally lends itself to being solved using SQL. Finally I wanted to demonstrate my capability 
of creating a more realistic, robust and scalable solution rather than a hacky collection of CSV munging scripts. 

To calculate the eligibility percentage I explored two different routes. Initially I intended to first determine a 
method of assigning a value to unknown answers based on the number of true and false responses to the same question, 
e.g. false chance = total false answers / total false answers + total true answers * 100. To calculate the 
overall eligibility chance you would then find all previous sessions that have matching answers to the current session, 
i.e. the same concrete answers where trues and falses are the same for each question, but unknowns can be anything, 
factor in the value assigned to unknowns for each of the matched sessions and then divide the total number of eligible 
answers with unknown value factored in again by this number to get the result. The problem with this approach is that 
in an attempt to assign a value to unknown answers, other unknown answers are in turn ignored. In addition to this you 
are also calculating this value based on individual questions, instead of looking at the individual answer sequences and 
determining the chance of that entire sequence being eligible or not. On reflection of this, it became apparent that in 
order to determine the eligibility chance of an individual sequence whilst factoring in a value for unknowns, the same 
approach must also be applied to all other sequences i.e. a recursive calculation of potentially infinite depth. After 
further thought I came to the conclusion that this would cancel itself out, and return a result the same as if unknowns 
were ignored completely. As such my final solution was to simply ignore the unknowns and take the total number of 
definitely eligible sessions divided by the total number of matching sessions as previously described. This can be seen 
with a more granular description in the `getEligibleChance` method.

Additionally I also considered attempting to determine unknown values based on answers to other questions e.g. non-smokers 
are less likely to have high blood pressure. Even simpler would have been to ask additional questions that could be used 
to determine the original answer. It's also possible that by using a patients session history the eligibility chance 
could be modified if their last session (or more?) was eligible, as they then maybe more likely to be eligible again. I 
decided that these approaches were probably out of the scope of the test.

When recording the answers I chose to store the unanswered questions (`U's`) in the database as well as the yesses (`T's`) 
and nos (`F's`). It could be argued that unanswered questions could simply have omitted rows in the answers table thus 
saving some disk space. I opted against this for ease of querying and completion of the data set, although i'm not sure 
it matters much either way.

Some of the queries used in the solution are quite complex, in particular `getEligibleChance` which entirely computes the 
eligibility chance percentage within SQL. An easier solution would have been a simple query to gather the required data 
from the database, and some Python code to then calculate the percentage from that data; this solution may also have 
been more readable from a code perspective. The reason I opted for the purely SQL route is two fold: the performance 
should be superior (although I did not benchmark this) since less data is being gathered and MySQL is optimized for 
these kinds of operations, and secondly it should also scale much more efficiently for larger data sets (although 
admittedly this isn't likely to be a problem for this task). I did perform some more exhaustive performance testing on 
the `getEligibleCount` query, although it transpired this method is mostly obsolete after I realised I could get the 
number of eligible patients at no extra cost as part of the `getEligibleChance` query, which was originally just 
obtaining the number of matching sessions.

With regards to testing, I attempted to hit most core functionality with exhaustive unit tests. In some cases, such as 
the ingest data script test, I also decided to use integration tests. An argument could be made for using both mock unit 
and integration testing to test the various database methods; this ensures both your code and the SQL behave as you 
expect. Without unit tests your code is not protected against potentially mis-executing queries and mis-handling 
arguments and validation, whereas without integration tests you cannot guarantee the SQL works as expected against 
real data. The downside of having both is of course the extra effort in writing the tests, setting up and tearing down 
the test database and the additional time taken for these tests to run.

What I Would Change With More Time
----------------------------------

The following is a brief list of things that I would have liked to implement given more time, in no particular order:

* A simple user interface for taking the questionnaire as opposed to the command line would have been nice, either as 
a desktop or web application.

* Better handling of the database with connection pools and transactions, this would then allow any code requiring the 
database to use a with statement for automatic handling of commits and the closing of connections.

* A better way of handling unknown values when calculating the eligibility chance, as described in the overview of the solution.

* Investigate making the services a bit more generic as there seems to be a fair amount of cross cutting concerns. It 
may also have been beneficial to use an ORM such as SQLAlchemy to remove the need for raw SQL and data mappers, 
however introducing an ORM brings a set of its own problems not necessarily worth the trade off.

* Patients should have to verify their identity when beginning the questionnaire using an e-mail or password to prevent 
anyone using their identity in subsequent sessions.

* Complex queries could have been improved by creating a view to query from.

* To improve architectural correctness, each service as it is now should actually be a DAO (data access object) 
responsible for direct interaction with the database. Each DAO should have an interface allowing it to be 
interchanged for a DAO of different implementation whilst still providing the same functionality, useful for instance
if data is to be provided from two different sources such as Amazon SDB and MySQL. The data retrieved by the DAOs should 
then by handed to a mapper class responsible for creating the Python objects from the data. Finally all remaining 
business logic should stay as a service, with additional methods exposing the operations provided by the DAOs along with 
any glue code that may be required. As with the DAOs, services should also have interfaces allowing for the 
interoperability of multiple implementations.

* User input should be validated when entering a name; currently non-alphabetic characters can be entered and it's 
likely to break if a name is too long. 

* A content management system or interactive mode would be useful for managing the entries in the database in a more 
usable manor, as well as for providing useful metrics. 

* Using a MySQL database does not scale effectively for large data sets with high throughput. As such it may be more 
effective to use an in-memory database such as Redis to temporarily record live answers from patients taking the 
questionnaire and then commit them to a database designed to store larger data sets such as Cassandra. 

* Integration tests for all methods interacting with the database.

* I had to convert the given csv data file into unix format from Windows as the Python CSV library was not playing nicely 
with Windows line endings on my Mac; I tried using an answer from StackOverflow[0] to fix this however that resulted in 
the values not being separated at all (basically the CSV library doing nothing!).

* As mentioned in the overview of the solution, integration testing requires a separate test database to be 
pre-configured. This should be done a bit smarter either by using an existing library or framework to take care of it 
or at least creating and destroying the database at the start and end of testing. 

* Patients do not enter any kind of uniquely identifiable information e.g. an e-mail or password. This means that when 
a patient reuses the system they could enter any name of a previous patient and assume their identity. It also means 
patients with the same name would end up sharing session histories. 

* There are currently no command line arguments; improved functionality may have been possible with additional options.

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
