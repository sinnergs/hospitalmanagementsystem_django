from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Diagnosticmaster,Diagnostictest
from deskexecutive.models import Userstore
def diagnosticHome(request):
	return render(request,"diagnostic/diagnosisHome.html")

def populateDiagnosticDB():
	ws_test_name=['ECG','Blood Test','MRI','CCTA','ECHO']
	ws_price=[700, 150, 1500,3200, 700]

	for i in range(len(ws_test_name)):
		addTest = Diagnosticmaster()
		addTest.ws_test_name=ws_test_name[i]
		addTest.ws_charge=ws_price[i]
		addTest.save()
def getDiagnosisList(ws_pat_id):
	diagnosisObj = Diagnostictest.objects.filter(ws_pat_id=ws_pat_id)
	diagnosisDict = []
	i=0
	cost=0
	for tests in diagnosisObj:
		testObj = get_object_or_404(Diagnosticmaster,ws_test_id=tests.ws_test_id)
		print(testObj.ws_test_id)
		diagnosisDict.append([testObj.ws_test_name,testObj.ws_charge])
		i+=1
		cost+=testObj.ws_charge
	return diagnosisDict, cost


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

def testDiagnose(request):
	if request.method == 'POST':
		pid = request.POST['pid']
		testId = request.POST['testid']
		if Diagnosticmaster.objects.filter(ws_test_id=testId).exists() and Userstore.objects.filter(ws_pat_id=pid).exists():
			ob = Diagnosticmaster.objects.filter(ws_test_id=testId)
			dt = Diagnostictest()
			dt.ws_pat_id = pid
			dt.ws_test_id = testId
			dt.save()
			return render(request,'diagnostic/testdiagnose.html',{'message':'Test Added Succesfully'})
		else:
			return render(request,'diagnostic/testdiagnose.html',{'message':"Test doesn't exists"})
	else:
		return render(request,'diagnostic/testdiagnose.html')

def add(request):
     if request.method == 'POST':
        testName = request.POST['testname']
        charges = request.POST['charge']
        print(testName,charges)
        ob = Diagnosticmaster()
        ob.ws_charge=charges
        ob.ws_test_name=testName
        ob.save()
        return redirect('diagnostic:diagnosticHome')
     else:   
        return render(request,'diagnostic/add.html')
        