from django.db import models
from django.contrib.postgres.fields import JSONField

class Epidemic(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="Flu")
    epidemic_type = models.CharField(max_length=50, default="trivial")
    total_infected = models.IntegerField(blank=False, default=0)
    cured = models.IntegerField(blank=False, default=0)
    died = models.IntegerField(blank=False, default=0)
    year = models.IntegerField(blank=False, default=2020)
    date = models.DateField(blank = True, null=True)
    police = models.IntegerField(blank=False, default=0)
    hospitalbeds = models.IntegerField(blank=False, default=0)
    healthstaff = models.IntegerField(blank=False, default=0)
    lesson_learnt = JSONField(blank=True, null=True)
    

def __str__(self):
        return self.title