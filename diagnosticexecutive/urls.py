from django.urls import path
from . import views
app_name="diagnostic"
urlpatterns=[
	path('',views.diagnosticHome,name="diagnosticHome"),
	path('adddiagnostictest/',views.add,name="addDiagnosticTest"),
	path('testdiagnose/',views.testDiagnose,name="testdiagnose"),
	path('testdiagnose/fetchdata',views.fetchData,name="fetchData"),
	# path('adddiagnosis/add',views.addDiagnosisTest,name="addDiagnosisTest"),
	
]