from django.contrib import admin
#from backend.dss import doables

# Register your models here.
from doables import models
admin.site.register(models.doable)

