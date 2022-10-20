from django.db import models
from .district import District
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    class Sex(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHER = "other"
    user = models.OneToOneField('auth.User', related_name="profile", on_delete=models.CASCADE, primary_key=True)
    sex = models.CharField(max_length=7, choices=Sex.choices, default=Sex.MALE)
    dob = models.DateField(blank=True)
    rank = models.CharField(max_length=25, blank=True)
    batch = models.PositiveSmallIntegerField(blank=True)
    district = models.ManyToManyField(District)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    mobileNumber = models.CharField(max_length=12, blank= True)
    departments= ArrayField(models.IntegerField(), null=True)
    def __str__(self):
        return self.user.first_name
