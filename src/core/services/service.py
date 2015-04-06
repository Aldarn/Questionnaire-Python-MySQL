import abc
from ..db import db

class Service (object):
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		self.db = db

	@abc.abstractmethod
	def create(self, obj):
		"""
		Creates the given object in the database.

		:param obj: Object to create.
		"""
		return
