from django.db import models
from django.contrib.postgres.fields import JSONField
from .events import Event


class LawAndOrder(models.Model):
    class SituationType(models.TextChoices):
        RALLY = "rally"
        GATHERING = "gathering"
        EPIDEMIC = "epidemic"
        CALAMITY = "calamity"
        CRIME = "crime"

    situation_type = models.CharField(max_length=15, choices=SituationType.choices, default=SituationType.RALLY)
    related_event = models.ForeignKey(Event, related_name='law_and_order', blank=True, null=True, on_delete=models.SET_NULL)
    configuration = JSONField(blank=False)
    arrangements = JSONField(blank=False)
