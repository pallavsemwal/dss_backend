from rest_framework import serializers 
from meetings.models import meetingGroup, meeting

class meetingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= meetingGroup
        fields=('groupId',
        'memberSecretary','committeeName','groupType',
        'isRecurring','recurringTime'
        )

class meetingSerializer(serializers.ModelSerializer):
    class Meta:
        model=meeting
        fields=('groupId','meetingId',
        'timestampCreation','minutesLink','meetingSubject',
        'noticeLink','scheduledTime'
        )