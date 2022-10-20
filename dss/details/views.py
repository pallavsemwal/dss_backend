from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
# from backend.dss.meetings.models import department
from rest_framework.decorators import permission_classes, authentication_classes
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, FileResponse, HttpRequest
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db import IntegrityError
from django.conf import settings
from .models.profile import Profile
from .models.district import District
from .models.eventsMaterials import EventFiles
import json
import datetime


@require_POST
def register_view(request):
    try:
        request_data = json.loads(request.body)
        print(request_data["district"])
        # for i in request_data["district"]:
        #     print("i", i["value"])
        new_user = User.objects.create_user(username=request_data["username"],
                                            password=request_data["password"],
                                            email=request_data["email"],
                                            first_name=request_data["first_name"],
                                            last_name=request_data["last_name"])


        profile_user = Profile(user=new_user,
                               departments=request_data['departments'],
                               sex=request_data["sex"]["value"],
                               dob=datetime.datetime.strptime(request_data["dob"], '%d-%m-%Y').date(),
                               rank=request_data["rank"],
                               batch=request_data["batch"], 
                               mobileNumber= request_data["mobileNumber"])
        profile_user.save()
        for dist in request_data["district"]:
            dist_obj = District.objects.get(pk=int(dist["value"]))
            print(dist_obj)
            profile_user.district.add(dist_obj)
    except IntegrityError as execption:
        print(str(execption))
        return HttpResponseBadRequest("User Already Exists With Same ID")
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to create user: Try Again")
    return HttpResponse("User Created")


@require_GET
def get_district_name_view(request):
    try:
        response = json.dumps(list(District.objects.values_list('id', 'name')))
        return HttpResponse(response, content_type='application/json')
    except Exception as e:
        print(str(e))
        return HttpResponseServerError("Some Server Side Error Occurs")

@require_GET
def get_file_view(request, file):
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(request)
        if user_jwt is not None:
            user = user_jwt[0]
            print(user)
            filename = settings.MEDIA_ROOT+'materials/'+file
            response = FileResponse(open(filename, 'rb')) 
            response['Content-Disposition'] = f'attachment; filename={file}'
            return response
        else:
            print(request.user, "User Not Authenticated.")
            return HttpResponseServerError("User Not Authenticated.")
    except Exception as e:
        print(str(e))
        return HttpResponseServerError("Some Server Side Error Occurs")
