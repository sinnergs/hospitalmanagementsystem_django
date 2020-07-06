from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import auth
from django.contrib.auth.models import User
# from .models import Staff
from pharmacist.views import populatePharmacistDB,getSize
from diagnosticexecutive.views import populateDiagnosticDB



def addStaff(request):
	if not request.user.is_authenticated:
		if getSize() == 0:
			populateDiagnosticDB()
			populatePharmacistDB()
		if request.method == "POST":
			name = request.POST['name']
			password = request.POST['password']
			email = request.POST['email'].lower()
			user = auth.authenticate(username=email,password=password)
			if user is None:
				user = User.objects.create_user(username=email,first_name=name,password=password)
				return redirect('staff:loginStaff')
			else:
				return render(request,'staff/register.html',{'error':'user already exist'})
		else:
			return render(request,'staff/register.html')
	else:
		return redirect('deskexecutive:deskHome')


def loginStaff(request):
		
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		user = auth.authenticate(username = email, password=password)
		if user is None:
			return render(request,'staff/login.html',{'error':'invalid ID password'})
		else:
			user = auth.authenticate(username = email, password=password)
			if user is None:
				return render(request,'staff/login.html',{'error':'invalid ID password'})
			else:
				auth.login(request,user)
				# user1 = get_object_or_404(User,pk = user.id)
				# if user1.staff.profession == "Desk Executive":
				# 	return redirect('deskexecutive:deskHome')
				# elif user1.staff.profession == "Pharmacist":
				# 	return redirect('pharmacist:pharmacistHome')
				# elif user1.staff.profession == "Diagnostic":
				# 	return redirect('diagnostic:diagnosticHome')
				return redirect('deskexecutive:deskHome')
	else:
		return render(request,'staff/login.html')

def logoutStaff(request):
	auth.logout(request)
	return render(request,'landingPage.html')