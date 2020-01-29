from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):
	return render(request,"index.html")


def Createuser(request):
	errorValidor = User.objects.userValidor(request.POST)
	if len(errorValidor) > 0:
		for key, value in errorValidor . items ():
			messages.error(request, value)
		return redirect("/")
	else:
		ashpassword = bcrypt.hashpw(request.POST["pw"].encode(),bcrypt.gensalt()).decode()
		usercreate = User.objects.create(name=request.POST["name"],username = request.POST["username"], password= ashpassword)
		print(usercreate)
		request.session["userID"] = usercreate.id
	return redirect("/travels")

def travels(request):
	user=User.objects.get(id=request.session["userID"])
	context = {
		"user":user,
		'myTrips':Trip.objects.filter(Q(created_by=user) | Q(participants=user)),
		"differenttrips" : Trip.objects.exclude(Q(created_by=user) | Q(participants=user)),
		"trips":Trip.objects.all()
	}
	return render(request,"travel.html", context)

def Login(request):
	errorValidor = User.objects.logindvalitor(request.POST)
	if len(errorValidor)>0:
		for key, value in errorValidor. items ():
			messages.error(request, value)
		return redirect("/")
	user =User.objects.get(username= request.POST['username'])
	request.session["userID"]= user.id
	return redirect("/travels")

def addTravels(request):
	return render( request, 'addtrip.html')
	
def createTrip(request):
	print(request.POST)
	tripvalidor = Trip.objects.tripValitor(request.POST)

	if len(tripvalidor)>0:
		for key, value in tripvalidor. items ():
			messages.error(request, value)
		return redirect("/travels/add")
	else:
		loggedinuser = User.objects.get(id = request.session["userID"] )
		createatrip = Trip.objects.create(destination = request.POST["destination"],description = request.POST["description"],startdate = request.POST["startdate"],enddate = request.POST["enddate"],created_by =loggedinuser)
		
		print(createatrip)
	return redirect("/travels")

def seeTrip(request,seeId):
    context = {
    "viweId":Trip.objects.get(id=seeId)
	}
    return render(request,"viewtrip.html", context)

def join(request,Id):
    loggedinuser = User.objects.get(id = request.session["userID"] )
    context ={
        "user":loggedinuser
    }
    trip = Trip.objects.get(id=Id)
    trip.participants.add(User.objects.get(id=request.session["userID"]))
    return redirect("/travels",context)

def logout(request):
	request.session.clear()
	return redirect("/")

   