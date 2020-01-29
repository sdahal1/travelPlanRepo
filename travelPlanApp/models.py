from django.db import models
import re
import bcrypt 
from datetime import datetime,  date
class UserManager(models.Manager):
	def userValidor(self,postDATA):

		errors = {}
		print(postDATA['username'])
		usernamelMatch = User.objects.filter(username = postDATA["username"])
		print(usernamelMatch)
		if len(postDATA["name"])< 2:
			errors["name"]= ' Name is Required  '
		if len(postDATA["username"])< 2:
			errors["username"]= 'User name is Required  '
		if len(postDATA["pw"])< 1:
			errors["pw"]= 'Password is requiered '
		elif len(postDATA["pw"])< 8:
			errors["pw"]= 'Password most be 8 more character '
		if postDATA["pw"] != postDATA["cpw"]:
			errors["cpw"]="password must macht!"
		if len(usernamelMatch)>0:
			errors['username']= "This username is already used , please use different Username"
			print (errors)
		return errors 

	def logindvalitor(self,postData):
		usernamelMatch = User.objects.filter(username = postData['username'])
		print(usernamelMatch)
		errors = {}
		if len(postData['username']) == 0:
			errors['usernamerequired'] = "username is Required "
		if len(usernamelMatch)==0:
			errors['userMatch']= "no user wiht this username"
		else:
			person = usernamelMatch[0]
			if bcrypt.checkpw(postData['pw'].encode(),person.password.encode()):
				print('password good')

			else:
				errors['pw'] = "password incorrect"
		return errors

class TripManager(models.Manager):
	def tripValitor(self,postDATA):
		time = datetime.now()
		now = time.strftime("%Y-%m-%d")
		errors = {}
		if len(postDATA["destination"])< 5:
			errors["Destination"]= ' Destination needs be more than 5 character '
			print(errors)
		if len(postDATA["description"])< 5:
			errors["description"]= ' Description needs be more than 5 character'
			print(errors)
		if len(postDATA["startdate"])< 1:
			errors["startdate"]= ' Date is require '
			print(errors)
		if len(postDATA["enddate"])< 1:
			errors["enddate"]= ' Trip end date is Required  '
			print(errors)
		if postDATA["startdate"] > postDATA['enddate']:
			errors["startdate"]="Choose a diferent date "
			print(errors)
		if postDATA["startdate"] < now:
			errors["startdate"]="Please don't enter a date in the past"
			print(errors)

		return errors
		

class User(models.Model):
	name=models.CharField(max_length=255,null=True)	
	username = models.CharField(max_length=255) 
	password= models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField(max_length=255)
	startdate = models.DateField(null=True)
	enddate = models.DateField(null=True)
	created_by = models.ForeignKey(User, related_name="created_trips",on_delete=models.CASCADE)
	participants = models.ManyToManyField(User, related_name="joined_trips")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripManager()
