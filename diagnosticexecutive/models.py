from django.db import models

class Diagnosticmaster(models.Model):
	ws_test_id = models.AutoField(primary_key=True, serialize = False)
	ws_test_name= models.CharField(max_length=255)
	ws_charge= models.FloatField()
	
	def __str__(self):
		return self.ws_test_name
	

class Diagnostictest(models.Model):
	ws_pat_id = models.IntegerField()
	ws_test_id = models.IntegerField()