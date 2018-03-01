from __future__ import unicode_literals
from django.db import models
from ..loginreg.models import User
from datetime import date, datetime

class TravelManager(models.Manager):
	def departureDate(self, date):
		today = datetime.strptime(str(date.today())[:10], '%Y-%m-%d')
		difference = (date - today).days
		if difference <= 0:
			return False
		else:
			return True
	def arrivalDate(self, departureDate, arrivalDate):
		difference = (arrivalDate - departureDate).days
		if difference <= 0:
			return False
		else:
			return True

class Travel(models.Model):
	destination = models.CharField(max_length = 255)
	start = models.DateTimeField()
	end = models.DateTimeField()
	schedule = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userss = models.ForeignKey(User, related_name = 'users_traveling')
	objects = TravelManager()

class UserTravel(models.Model):
	user = models.ForeignKey(User, related_name="total_users")
	travel = models.ForeignKey(Travel, related_name="total_travel")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)