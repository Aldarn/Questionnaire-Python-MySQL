import abc
from ..db import DB

class Service (object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def save(self, obj):
		"""
		Saves the given object in the database.

		:param obj: Object to save.
		"""
		return
