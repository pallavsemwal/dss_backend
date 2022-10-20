from django.db import models
from django.contrib.postgres.fields import JSONField
from .tags import Tag


class Event(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1
        NORMAL = 2
        HIGH = 3

    owner = models.ForeignKey('auth.User', related_name='events', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=70, blank=False)
    is_all_day = models.BooleanField(default=False)
    start_date_time = models.DateTimeField(blank=False)
    '''
        https://stackoverflow.com/questions/48388366/i-want-to-add-a-location-field-in-django-model-which-take-location-input-by-putt
        location field can be made like this as well but since location can't be always found
        Format of location = 'is_lat_long,latitude,longitude'
    '''
    location = models.CharField(max_length=30, blank=True)
    end_date_time = models.DateTimeField(blank=False)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NORMAL)
    creation_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="events_of_tag", blank=True)
    mom = JSONField(blank=True, null=True)
    recipients = models.ManyToManyField('auth.User', blank=True, related_name="shared_with_me_events")

    class Meta:
        ordering = ['start_date_time']

    def __str__(self):
        return self.event_name
