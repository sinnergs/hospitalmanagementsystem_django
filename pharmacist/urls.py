from django.urls import path
from . import views
app_name= "pharmacist"
urlpatterns=[
	path('',views.pharmacistHome,name="pharmacistHome"),	
	path('addmedicine/',views.addMedicine,name="addMedicine"),
	path('getpatientid/',views.getPatientId,name="getPatientId"),
	path('getpatientid/issuemedicine/',views.issueMedicine, name="issueMedicine"),
	path('getpatientid/issuemedicine/getmedlist/',views.getMedList, name="getMedList"),
]