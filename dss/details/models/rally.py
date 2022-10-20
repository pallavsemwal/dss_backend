from django.db import models
from django.contrib.postgres.fields import JSONField

class Rally(models.Model):

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rally_title = models.CharField(max_length=40, blank=False)
    religious = models.BooleanField(default=False)
    political = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    protest = models.BooleanField(default=False)
    government = models.BooleanField(default=False)
    attendance = models.IntegerField(blank=False)
    stationary = models.BooleanField(default = False)
    start_location = models.CharField( max_length=50, blank = False)
    end_location = models.CharField(max_length=50, blank = True, null=True )
    police = models.IntegerField(blank=False, default=0)
    ambulance = models.IntegerField(blank=False, default=0)
    firefighters = models.IntegerField(blank=False, default=0)
    date = models.DateField(blank=True, null=True)
    lessons_learnt = JSONField(blank = True, null = True)

def __str__(self):
        return self.rally_title