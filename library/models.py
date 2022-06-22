from django.db import models

# Create your models here.
class user(models.Model):
    sroll=models.IntegerField()
    spwd=models.CharField(max_length=10)

class books(models.Model):
    sbookname=models.CharField(max_length=10)
    sbookcount=models.IntegerField()

class transaction(models.Model):
    sroll=models.IntegerField()
    sbookname=models.CharField(max_length=10)
    sstatus=models.CharField(max_length=10)   #has values requested, accepted or rejected