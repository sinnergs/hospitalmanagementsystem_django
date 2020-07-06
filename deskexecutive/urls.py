from django.urls import path
from . import views

app_name = "deskexecutive"  #stored in app_name so that it can be called from anywhere
urlpatterns = [
	path('',views.deskHome, name='deskHome'),
	path('addpatient/',views.addPatient,name="addPatient"),
	path('getallpatient/',views.showAllPatient,name = "showAllPatient"),
	path('updatepatient/',views.updatePatient,name="updatePatient"),
	path('deletepatient/',views.deletePatient,name="deletePatient"),
	path('deletepatient/fetchData/',views.fetchData,name="fetchDeleteData"),
	path('updatepatient/fetchData/',views.fetchData,name="fetchUpdateData"),
	path('billing/fetchactivepatient/',views.fetchActivePatient,name="fetchActivePatient"),
	path('billing/',views.billing,name="billing"),
	path('checkout/',views.checkout,name="checkout"),
	path('searchpatient/',views.searchPatient,name="searchPatient"),
] 

