from django.db import models
from .district import District


class Scheme(models.Model):
    name = models.CharField(max_length=30, blank=False)
    district = models.ForeignKey(District, related_name='schemes', on_delete=models.SET_NULL, null=True)
    details = models.TextField(blank=True)
    num_people_reached = models.IntegerField(default=0)
    num_people_left = models.IntegerField(default=0)
    image = models.ImageField(upload_to='schemes/', default='schemes/default.jpg')

    class Meta:
        ordering = ['-num_people_reached']

    def __str__(self):
        return self.name
