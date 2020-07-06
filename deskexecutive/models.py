from django.db import models
from django.utils import timezone

class Userstore(models.Model):
	ws_ssn = models.IntegerField()
	ws_pat_id = models.AutoField(primary_key=True, serialize = False)
	ws_pat_name = models.CharField(max_length=255)
	ws_pat_age= models.IntegerField()
	ws_city = models.CharField(max_length=100)
	ws_state = models.CharField(max_length=100)
	ws_adrs = models.CharField(max_length=300)
	ws_status = models.CharField(max_length=60, default="Active")
	ws_doj = models.DateTimeField(default = timezone.now)
	ws_rtype = models.CharField(max_length=30)
	def __str__(self):
		return self.ws_pat_name

	def prettyTime(self):
		return self.ws_doj.strftime("%Y/%m/%d")