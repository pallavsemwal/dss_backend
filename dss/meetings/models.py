from ctypes import Array
import datetime
from enum import unique
from tkinter import CASCADE
from django.db import models
import uuid
from django.contrib.postgres.fields import JSONField
from doables.models import doable
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

# Create your models here.
class meetingGroup(models.Model):
    groupId= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memberSecretary= models.ForeignKey(get_user_model(),on_delete= models.CASCADE, blank=True)
    committeeName= models.CharField(blank=False, max_length=1000)
    groupType= models.BooleanField(default=False) # 0->Committee meetings 1->ad hoc
    isRecurring= models.BooleanField(default=True) # 0->If not recurring
    recurringTime= models.IntegerField(default=30) # inDays
    groupMembers= ArrayField(models.IntegerField(), null=True)
    relatedDepartmentId=ArrayField(models.IntegerField(), null=True)


class meeting(models.Model):
    meetingId= models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    groupId= models.ForeignKey(meetingGroup,on_delete=models.CASCADE)
    timestampCreation= models.DateTimeField(max_length=50)
    minutesOfMeeting= models.TextField(null=True)
    minutesLink = models.CharField(max_length=1000, default="")
    meetingSubject= models.CharField(max_length=1000,blank=False)
    scheduledTime= models.DateTimeField(max_length=50)
    noticeLink= models.CharField(max_length=1000,default="")
    doablesAssigned= ArrayField(models.UUIDField(), null= True)
    agenda=JSONField(null=True)

class document(models.Model):
    documentId=models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    meetingId=models.ForeignKey(meeting,on_delete=models.CASCADE)
    documentLink=models.CharField(max_length=1000,null=False)
    uploadedBy=models.IntegerField(null=False)

     
