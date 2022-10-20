from django.db import models
from django.contrib.postgres.fields import JSONField

class Calamity(models.Model):
    class CalamityTypes(models.TextChoices):
        FLOODS = "Floods"
        DROUGHT =  "Drought"
        EARTHQUAKE = "Earthquake"
        FORESTFIRE = "Forest Fire"
        CYCLONE = "Cyclone"
        LANDSLIDE = "Landslide"
        STORM = "Storm"
        OTHER = "Other"

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    calamity_type = models.CharField(max_length=20, choices=CalamityTypes.choices, default=CalamityTypes.OTHER)
    total_cost = models.BigIntegerField(default=0)
    injured = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    people_affected = models.IntegerField(default=0)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    police = models.IntegerField(blank=False, default=0)
    ambulance = models.IntegerField(blank=False, default=0)
    ndrf = models.IntegerField(blank=False, default=0)
    lesson_learnt = JSONField(null = True, blank = True)


def __str__(self):
        return self.title

