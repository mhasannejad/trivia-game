from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(Subject)
admin.site.register(Option)
admin.site.register(Challenge)
admin.site.register(Question)
admin.site.register(UserAnswerSubmit)
