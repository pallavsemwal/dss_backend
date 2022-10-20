"""dss URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from details.views import register_view, get_district_name_view, get_file_view
from details.viewsProd import index
from graphene_file_upload.django import FileUploadGraphQLView

#TODO not csrf exempt, similary for graphql not csrf exempt: https://www.techiediaries.com/django-react-forms-csrf-axios/
urlpatterns = [
    path('', index),
    path('login', index),
    path('logout', index),
    path('signup', index),
    path('thanks', index),
    path('user/', index),
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('getDistrictNames/', get_district_name_view),
    path('register/', csrf_exempt(register_view)),
    path('media/<str:file>', csrf_exempt(get_file_view)),
]