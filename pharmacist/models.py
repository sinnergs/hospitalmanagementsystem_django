from django.db import models

class Medicinemaster(models.Model):
	ws_med_id = models.AutoField(primary_key=True, serialize = False)
	ws_med_name= models.CharField(max_length=255)
	ws_stock_qty = models.IntegerField() 
	ws_price= models.FloatField()

	def __str__(self):
		return self.ws_med_name
	

class Medicineissued(models.Model):
	ws_pat_id = models.IntegerField()
	ws_med_id = models.IntegerField()
	ws_qty = models.IntegerField()
