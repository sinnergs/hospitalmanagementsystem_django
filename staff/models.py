from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Staff(models.Model):
# 	user = models.OneToOneField(User,on_delete=models.CASCADE)
# 	profession= models.CharField(max_length=100)
