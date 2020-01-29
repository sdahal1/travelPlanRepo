from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
    path('createaccount',views.Createuser),
    path("travels",views.travels),
    path("userlogin",views.Login),
	path("travels/add",views.addTravels),
	path('createTrip', views.createTrip),	
	path("travels/destination/<seeId>",views.seeTrip),
    path("travels/join/<Id>", views.join),
	path('logout', views.logout)
]
