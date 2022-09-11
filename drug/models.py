from django.db import models


# Create your models here.
class Drug(models.Model):
    name = models.CharField(max_length=555, default='')


class DrugSubsets(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True)
    melh = models.CharField(max_length=255, default='')
    drug_form = models.CharField(max_length=255, default='')
    dose = models.CharField(max_length=255, default='')
    route_of_admin = models.CharField(max_length=255, default='')
    atc_code = models.CharField(max_length=255, default='')
    ingredient = models.CharField(max_length=255, default='')
    clinical = models.CharField(max_length=255, default='')
    access_level = models.CharField(max_length=255, default='')
    remarks = models.CharField(max_length=255, default='')
    date = models.CharField(max_length=255, default='')


class Prescription(models.Model):
    image = models.ImageField(upload_to='prescriptions')


class PrescriptionItem(models.Model):
    drug = models.ForeignKey(DrugSubsets, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(null=True)
    per_time = models.CharField(max_length=255, null=True)


