from django.db import models
class department(models.Model):
    departmentId=models.AutoField(primary_key=True)
    departmentName=models.CharField(max_length=1000,editable=False,null=False)