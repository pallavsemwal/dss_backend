from rest_framework import serializers 
from message.models import message

class messageSerializer(serializers.ModelSerializer):
    class Meta:
        model=message
        fields=('messageId','senderId','receiverId','messageType','messageContent','relatedDocumentLink',
        'timestampCreation','doableId'
        )