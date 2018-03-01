from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
	def validate(self, postData):
		alert = True
		errors = []
		if len(postData['name']) < 3:
			alert = False
			errors.append('Name field has to be greater than 3 characters')
		if len(postData['user_name']) < 3:
			alert = False
			errors.append('Username field has to be greater than 3 characters')
		if len(postData['password']) < 8:
			alert = False
			errors.append('Password must be atleast 8 characters long')
		if postData['password_confirm'] != postData['password']:
			alert = False
			errors.append('Passwords must match')

		if alert:
			password = postData['password']
			hashed = bcrypt.hashpw(str(password), bcrypt.gensalt())
			user = User.objects.create(
				name=postData['name'], 
				username=postData['user_name'], 
				password=hashed
			)
			return (True, user)
		else:
			return (False, errors)

class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
	objects = UserManager()