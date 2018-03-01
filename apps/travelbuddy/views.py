from django.shortcuts import render, redirect, HttpResponse
from .models import User, Travel, UserTravel, TravelManager
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import date, datetime

# this function gets all user info, all the trips, and all the trips user is not going to
def index(request):
	user = User.objects.get(id = request.session['user']) # finds a user currently in session
	context = {
		'user': User.objects.get(id = request.session['user']), 
		'userTrips': Travel.objects.filter(total_travel__user = user), #gets a count of objects of trips of current user
		'totalTrips': Travel.objects.all().exclude(total_travel__user = user) #gets a count of objects of all trips
	}
	print context['totalTrips']
	return render(request, 'travelbuddy/index.html', context)

# this function renders schedule template
def schedule(request):
	return render(request, 'travelbuddy/schedule.html')

# this function creates a trip for the user
def createTrip(request):
	if request.method == 'POST':
		alert = True
		departureDate = datetime.strptime(str(request.POST['start'])[:10], '%Y-%m-%d')
		arrivalDate = datetime.strptime(str(request.POST['end'])[:10], '%Y-%m-%d')
		user = User.objects.get(id = request.session['user'])	

		if not Travel.objects.departureDate(departureDate):
			alert = False
			messages.error(request, 'Departure date entry is not correct, it has to be in the future')
		if not Travel.objects.arrivalDate(departureDate, arrivalDate):
			alert = False
			messages.error(request, 'Arrival date entry is not correct, it has to be after departure date')

		if alert:
			trip = Travel.objects.create(
				destination=request.POST['destination'], 
				start=request.POST['start'], 
				end=request.POST['end'], 
				schedule=request.POST['description'], 
				userss=user
			)

			user = User.objects.get(id = request.session['user'])
			UserTravel.objects.create(user=user, travel=trip)
			return redirect(reverse('buddy:home'))
		
	return redirect(reverse('buddy:schedule'))

# this function show user travel plans and otherpeople's travel plans
def show(request, id):
	user = User.objects.filter(total_users__id = id)
	travel = Travel.objects.get(id= id)
	context = {
		'user': User.objects.get(id = request.session['user']),
		'userTrips': UserTravel.objects.get(id = id),
		'otherpeople': UserTravel.objects.filter(travel=travel).exclude(user=user)
	}
	return render(request, 'travelbuddy/show.html', context)

# This function let's the user join the trip
def join(request, id):
	user = User.objects.get(id = request.session['user'])
	trip = Travel.objects.get(id=id)
	check = UserTravel.objects.filter(user=user).filter(travel=trip)
	if not check:
		UserTravel.objects.create(user=user, travel=trip)
	else:
		messages.error(request, "You already going!")
	return redirect(reverse('buddy:home'))