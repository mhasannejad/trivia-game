from django.contrib import admin

# Register your models here.
from leitner.models import *

admin.site.register(Daroo)
admin.site.register(FlashCard)
admin.site.register(Card)
admin.site.register(Pharma)