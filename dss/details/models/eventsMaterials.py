from django.db import models
from .events import Event


class EventFiles(models.Model):
    file = models.FileField(upload_to='materials/')
    event = models.ForeignKey(Event, related_name="files", null=True, on_delete=models.SET_NULL)
