from django.urls import path

from . import views
 
urlpatterns = [ 
    path('createMessage', views.create_message),
    # path('createMeeting', views.createMeeting, name="createMeeting"),
    # path('getUsers',views.getAllUsers),
    # path('getMeetingGroups',views.getAllMeetingsGroup),
    # path('create', views.createNotice)
]