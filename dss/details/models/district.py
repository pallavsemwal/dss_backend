from django.db import models


class District(models.Model):
    name = models.CharField(max_length=20, blank=False)
    area = models.IntegerField(blank=True)
    state = models.CharField(max_length=20, blank=False)
    # In the latitude longitude format
    location = models.CharField(max_length=25, blank=True)
    population = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
