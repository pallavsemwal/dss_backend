from django.db import models
import uuid
import datetime
from django.contrib.auth import get_user_model
#from sqlalchemy import null
from doables.models import doable
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class message(models.Model):
    class messageTypes(models.TextChoices):    
        notice="notice"
        doable="doable"


    messageId=models.CharField(primary_key=True, max_length=1000,editable=False)  #primary key
    senderId=models.IntegerField(null=False)   
    receiverId=models.IntegerField(null=False) 
    messageType=models.CharField(max_length=20, choices=messageTypes.choices, default=messageTypes.notice)
    
    messageContent=models.CharField(max_length=1000)  #for notice subject, for doable related doable
    relatedDocumentLink=models.CharField(max_length=1000)  #incase of notice pdflink, for doable document link if any
    timestampCreation= models.DateTimeField(max_length=10)
    doableId=models.UUIDField(null=True)     

