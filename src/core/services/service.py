import abc
from ..db import db

class Service (object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def create(self, obj):
		"""
		Creates the given object in the database.

		:param obj: Object to create.
		"""
		return
