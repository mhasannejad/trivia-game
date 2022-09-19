from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Drug)
admin.site.register(DrugSubsets)
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(PrescriptionVerification)