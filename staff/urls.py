from django.urls import path
from . import views
app_name = "staff"
urlpatterns=[
	path('',views.loginStaff,name="staffHome"),
	path('addstaff/',views.addStaff,name="addStaff"),
	path('logout/',views.logoutStaff,name="logoutStaff"),
	path('loginstaff/',views.loginStaff,name="loginStaff"),
]