from email.policy import default
from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from django.contrib.auth import get_user_model
# Create your models here.
class doable(models.Model):
    class doableTypes(models.TextChoices):
        compliance= "compliance"
        meeting= "meeting"
    doableId= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deadline= models.DateTimeField()
    completed= models.BooleanField(default=False)
    reminderPeriod= models.IntegerField(default=10)
    assignedTo= models.IntegerField()
    assignedBy= models.IntegerField()
    subject = JSONField()
    doableType=models.CharField(max_length=20, choices=doableTypes.choices, default=doableTypes.meeting)
    typeId= models.UUIDField( null=True)   #meeting id
    