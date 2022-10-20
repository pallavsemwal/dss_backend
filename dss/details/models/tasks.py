from django.db import models


class Task(models.Model):
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50, blank=False)
    task_date = models.DateField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['task_date']
    def __str__(self):
        return self.task_name