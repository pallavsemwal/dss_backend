# from attr import field
from rest_framework import serializers 
from doables.models import doable

class doableSerializer(serializers.ModelSerializer):
    class Meta:
        model=doable
        fields=('doableId','deadline','completed','reminderPeriod','assignedTo','assignedBy','subject','doableType','typeId')