from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Userstore
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from pharmacist.views import getMedicineList
from diagnosticexecutive.views import getDiagnosisList

def deskHome(request):  #Deskexecutive HomePage after login 
	return render(request,'deskexecutive/deskHome.html')

def addPatient(request):
	if request.method == "POST":  # checking whether data coming is from post request or not
		# now store all the details from the user in the database
		ssnid = request.POST['ssnid']
		age = request.POST['age']
		name = request.POST['name']
		roomtype = request.POST['roomtype']
		adrs = request.POST['adrs']
		city = request.POST['city']
		state = request.POST['state']
		patientobj = Userstore() #Creating object of the userstore database
		patientobj.ws_ssn = ssnid
		patientobj.ws_pat_name = name
		patientobj.ws_pat_age = age
		patientobj.ws_city = city
		patientobj.ws_state = state
		patientobj.ws_adrs = adrs
		patientobj.ws_status = "Active"
		patientobj.ws_rtype = roomtype
		patientobj.save()
		return redirect('deskexecutive:deskHome') #After adding patient desk executive will be redirected to the Desk executive's Home page 
	else:
		return render(request,'deskexecutive/addPatient.html')

def showAllPatient(request):
	user = Userstore.objects  # Getting objects of all the patient in our database
	return render(request,'deskexecutive/showAllPatient.html',{'user':user})

def updatePatient(request):
	if request.method == "POST":
		ws_pat_id=request.POST['uid']
		patientobj = Userstore.objects.get(ws_pat_id=ws_pat_id)

		if request.POST['age']!= patientobj.ws_pat_age:
			patientobj.ws_pat_age = request.POST['age']
		if request.POST['name']!=patientobj.ws_pat_name:
			patientobj.ws_pat_name = request.POST['name']
		if request.POST['roomtype']!=patientobj.ws_rtype:
			patientobj.ws_rtype = request.POST['roomtype']
		if request.POST['adrs']!=patientobj.ws_adrs:
			patientobj.ws_adrs = request.POST['adrs']
		if request.POST['city']!=patientobj.ws_city:
			patientobj.ws_city = request.POST['city']
		if request.POST['state']!=patientobj.ws_state:
			patientobj.ws_state = request.POST['state']
		patientobj.save()
		return redirect('deskexecutive:deskHome')
	else:
		return render(request,'deskexecutive/updatePatient.html')

def deletePatient(request):
	if request.method == "POST":
		ws_pat_id = request.POST['uid']
		patientobj = Userstore.objects.get(ws_pat_id=ws_pat_id)
		# Userstore.objects.filter(ws_pat_id=ws_pat_id).delete()
		patientobj.delete()
		return redirect('deskexecutive:deskHome')
	else:
		return render(request,"deskexecutive/deletePatient.html")


@csrf_exempt
def fetchData(request):
	if request.method == "POST":
		ws_pat_id = request.POST['uid']
		patientobj= get_object_or_404(Userstore,pk=ws_pat_id)

		patientDetails={
		'patientId' : ws_pat_id,
		'patientName': patientobj.ws_pat_name,
		'patientSSN' : patientobj.ws_ssn,
		'patientAge' : patientobj.ws_pat_age,
		'patientCity': patientobj.ws_city,
		'patientState': patientobj.ws_state,
		'patientAdrs' : patientobj.ws_adrs,
		'patientStatus': patientobj.ws_status,
		'patientRtype' : patientobj.ws_rtype,
		'patientDOJ' : str(patientobj.prettyTime)
		}
	return HttpResponse(json.dumps(patientDetails))

@csrf_exempt
def fetchActivePatient(request):
	if request.method == "GET":
		ws_pat_id = request.GET['uid']
		if not (Userstore.objects.filter(ws_pat_id=ws_pat_id).exists()):
			return HttpResponse(json.dumps({'exists':'no'}))
		patientobj= get_object_or_404(Userstore,pk=ws_pat_id)
		patientDetails={
		'exists':'yes',
		'patientId' : ws_pat_id,
		'patientName': patientobj.ws_pat_name,
		'patientSSN' : patientobj.ws_ssn,
		'patientAge' : patientobj.ws_pat_age,
		'patientCity': patientobj.ws_city,
		'patientState': patientobj.ws_state,
		'patientAdrs' : patientobj.ws_adrs,
		'patientStatus': patientobj.ws_status,
		'patientRtype' : patientobj.ws_rtype,
		'patientDOJ' : str(patientobj.prettyTime)
		}
	return HttpResponse(json.dumps(patientDetails))


def billing(request):
	if request.method == "POST":
		pass
	else:
		return render(request,"deskexecutive/billing.html")

@csrf_exempt
def checkout(request):
	if request.method=="GET":
		pid = request.GET['uid']
		patientobj = get_object_or_404(Userstore,ws_pat_id=pid)
		days = str(timezone.now() - patientobj.ws_doj)
		try:

			days = int(days[0:days.index(" ")])+1
		except :
			days=1
		if (patientobj.ws_rtype == "General Ward"):
			bedPrice=2000*days
		elif (patientobj.ws_rtype=="Semi-Sharing"):
			bedPrice= days*4000
		else:
			bedPrice=days*8000
		patientDetails={
		'patientId' : patientobj.ws_pat_id,
		'patientName': patientobj.ws_pat_name,
		'patientSSN' : patientobj.ws_ssn,
		'patientRtype' : patientobj.ws_rtype,
		'patientAge' : patientobj.ws_pat_age,
		'patientAdrs' : patientobj.ws_adrs,
		'patientCity': patientobj.ws_city,
		'patientDOJ' : str(patientobj.prettyTime())
		}
		DiagnosTest, testcost= getDiagnosisList(pid)
		medicine, medcost = getMedicineList(pid)
		print(medicine)
		print(DiagnosTest)
		bedDetails={
		'days':days,
		'bedPrice':bedPrice
		}
		return render(request,'deskexecutive/checkout.html',{"total":medcost+testcost+bedPrice,"medcost":medcost,"testcost":testcost,"patientDetails":patientDetails,'days':days,'bedPrice':bedPrice,'medicine':medicine,'DiagnosTest':DiagnosTest})
	elif request.method=="POST":
			pid = request.POST['pid']
			patientObj = Userstore.objects.get(ws_pat_id=pid)
			patientObj.ws_status = "Discharged"
			patientObj.save()
			return redirect("deskexecutive:deskHome")
			

@csrf_exempt
def searchPatient(request):
	if request.method=="POST":
		ws_pat_id = request.POST['uid']
		if not (Userstore.objects.filter(ws_pat_id=ws_pat_id).exists()):
			return HttpResponse(json.dumps({'exists':'no'}))
		patientobj= get_object_or_404(Userstore,pk=ws_pat_id)
		patientDetails={
		'exists':'yes',
		'patientId' : ws_pat_id,
		'patientName': patientobj.ws_pat_name,
		'patientSSN' : patientobj.ws_ssn,
		'patientAge' : patientobj.ws_pat_age,
		'patientCity': patientobj.ws_city,
		'patientState': patientobj.ws_state,
		'patientAdrs' : patientobj.ws_adrs,
		'patientStatus': patientobj.ws_status,
		'patientRtype' : patientobj.ws_rtype,
		'patientDOJ' : str(patientobj.prettyTime)
		}
		return HttpResponse(json.dumps(patientDetails))
	else:
		return render(request,'deskexecutive/searchPatient.html')
