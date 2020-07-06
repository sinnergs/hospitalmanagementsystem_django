from django.shortcuts import render,get_object_or_404,redirect
from .models import Medicinemaster, Medicineissued
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from deskexecutive.models import Userstore
def getSize():
	count_medicine_rows = Medicinemaster.objects.count()
	return count_medicine_rows
def populatePharmacistDB():
	ws_med_name=['Paracetamol','Crocin','Disprin']
	ws_price=[73,20,50]
	ws_stock_qty=[90,100,30]
	for i in range(len(ws_med_name)):
		addStock = Medicinemaster()
		addStock.ws_med_name=ws_med_name[i]
		addStock.ws_stock_qty=ws_stock_qty[i]
		addStock.ws_price=ws_price[i]
		addStock.save()
def getMedicineList(ws_pat_id):
	medicineissuedobj = Medicineissued.objects.filter(ws_pat_id=ws_pat_id)
	medicineDict = []
	i=0
	cost =0
	for meds in medicineissuedobj:
		priceObj = get_object_or_404(Medicinemaster,ws_med_id=meds.ws_med_id)
		print(priceObj.ws_med_id)
		medicineDict.append([priceObj.ws_med_name,meds.ws_qty,priceObj.ws_price,priceObj.ws_price*meds.ws_qty])
		i+=1
		cost+=priceObj.ws_price*meds.ws_qty
	return medicineDict, cost
def pharmacistHome(request):
	return render(request,"pharmacist/pharmacistHome.html")

@csrf_exempt
def issueMedicine(request):
	if request.method == "POST":
		pid = request.POST['pid']
		medid=request.POST['medid']
		medqty = request.POST['qty']
		if Medicinemaster.objects.filter(ws_med_id=medid).exists() and Userstore.objects.filter(ws_pat_id=pid).exists():
			medobj = Medicineissued()
			medobj.ws_med_id=medid
			medobj.ws_pat_id = pid
			medobj.ws_qty = medqty
			medobj.save()
			updateMaster = get_object_or_404(Medicinemaster,ws_med_id=medid)
			updateMaster.ws_stock_qty -= int(medqty)
			updateMaster.save()
			print("Success")
			return HttpResponse("success")
		else:
			return HttpResponse("medid_err")
	else:
		pid = request.GET['pid']
		if Userstore.objects.filter(ws_pat_id=pid).exists():
			patientobj= get_object_or_404(Userstore,pk=pid)
			patientDetails={
			'patientId' : pid,
			'patientName': patientobj.ws_pat_name,
			'patientSSN' : patientobj.ws_ssn,
			'patientAge' : patientobj.ws_pat_age,
			'patientRtype' : patientobj.ws_rtype,
			'patientDOJ' : str(patientobj.prettyTime())
			}
			medList, cost = getMedicineList(pid)
			return render(request,'pharmacist/issuemedicine.html',{'medicine':medList,'patientDetails':patientDetails,'name':["amnsih","Ajat"]})

def addMedicine(request):
	if request.method == "POST":
		medicineName= request.POST['medName']
		medicineStockQuantity = request.POST['medStckQty']
		medicinePrice = request.POST['medPrice']
		addStock = Medicinemaster()
		addStock.ws_med_name= medicineName
		addStock.ws_stock_qty=medicineStockQuantity
		addStock.ws_price=medicinePrice
		addStock.save()
		return redirect('pharmacist:pharmacistHome')
	else:
		return render(request,"pharmacist/addMedicineStock.html")

def getPatientId(request):
	return render(request,'pharmacist/getPatientId.html')

@csrf_exempt
def getMedList(request):
	if request.method=="POST":
		medList = {}
		medobj = Medicinemaster.objects.all()
		i=0
		for meds in medobj:
			medList[i]=[meds.ws_med_name, meds.ws_med_id, meds.ws_stock_qty, meds.ws_price]
			i+=1
		medList['len']=i
		print(medList)
		return HttpResponse(json.dumps(medList))





