from django.urls import path

from . import views
 
urlpatterns = [ 
    path('createMeetingGroup', views.createMeetingGroup, name='createMeetingGroup'),
    path('createMeeting', views.createMeeting, name="createMeeting"),
    path('getUsers',views.getAllUsers),
    path('getMeetingGroups',views.getAllMeetingsGroup),
    path('createNotice', views.createNotice),
    path('allDepartment',views.allDepartment),
    path('upcomingMeetings',views.upcomingMeetings),
    path('allMeetingGroup',views.allMeetingGroup),
    path('meetingGroupDetails',views.meetingGroupDetails),
    path('meetingGroupDoable',views.meetingGroupDoable),
    path('meetingDetail',views.meetingDetail),
    path('updateMeetingGroup',views.updateMeetingGroup),
    path('totalMeeting',views.totalMeeting),
    path('doableCount',views.doableCount),
    path('rescheduleMeeting',views.rescheduleMeeting),
    path('deleteMeetingGroup',views.deleteMeetingGroup),
    path('deleteMeeting',views.deleteMeeting)
]
