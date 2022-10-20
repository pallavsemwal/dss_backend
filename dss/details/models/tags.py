from django.db import models


class Tag(models.Model):
    owner = models.ForeignKey('auth.User', related_name="own_tags", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, blank=False)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.name
