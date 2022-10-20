from statistics import mode
from django.contrib import admin
from meetings import models
admin.site.register(models.meeting)
admin.site.register(models.meetingGroup)
admin.site.register(models.document)
# Register your models here.
