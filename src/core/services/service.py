import abc
from ..db import dbInstance

class Service (object):
	__metaclass__ = abc.ABCMeta

	# Static db instance for the convenience of child classes
	db = dbInstance

	def __init__(self):
		pass

	@abc.abstractmethod
	def create(self, obj):
		"""
		Creates the given object in the database.

		:param obj: Object to create.
		"""
		return

	@abc.abstractmethod
	def _map(self, databaseResult):
		"""
		Maps the given database result to an instance of an object.

		:param databaseResult: The result of a database query
		"""
		return

class NoResultFound(Exception):
	pass
