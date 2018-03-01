from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	return render(request, 'loginreg/index.html')

def register(request):
	data = {
		"name" : request.POST['name'],
		"user_name" : request.POST['user_name'],
		"password" : request.POST['password'],
		"password_confirm" : request.POST['password_confirm']
	}

	result = User.objects.validate(data)

	if result[0]:
		request.session['user_id'] = result[1].id 
		context = {
			'success': "You have Succesfully Registered!"
		}
		return render(request, 'loginreg/index.html', context)
	else:
		for err in result[1]:
			messages.error(request, err)
		return redirect('/')

def login(request):
	if request.method == 'POST':
		username = request.POST['user_name']
		password = request.POST['password']

		if not User.objects.filter(username=username):
			context = {
				'error': 'Username Not Found'
			}
			return render(request, 'loginreg/index.html', context)

		user = User.objects.filter(username=username)

		if bcrypt.hashpw(str(password), str(user[0].password)) == user[0].password:
			request.session['user'] = user[0].id
		else:
			context = {
				'pass': "Password is not correct"
			}
			return render(request, 'loginreg/index.html', context)
	
		return redirect(reverse('buddy:home'))

def logout(request):
	request.session.clear()
	return redirect('/')