from datetime import datetime
from http.client import HTTPResponse
# from sys import ps2
from telnetlib import STATUS
from django.shortcuts import render
import uuid
# from sympy import content
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.core import serializers
from doables.serializer import doableSerializer
from requests import Session
import json
from .models import doable
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, FileResponse, HttpRequest
from django.db import IntegrityError
from message.views import create_message
from details.models.profile import Profile
from meetings.views import dictfetchall
from django.db import connection
from message.models import message
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['POST'])
def create_doable(request):
    d= JSONParser().parse(request)
    d["assignedBy"]=request.user.pk
    print(d)
    del d["memberName"]
    # did=uuid.uuid1()
    do= doable.objects.create(**d)
    d["doableId"]=do.pk
    # serializer = doableSerializer(data=d)
        #serializer.save()
        #print("doable created")

        #creating request to create_message
    #URL="http://127.0.0.1:8000/message/createMessage"
    relatedDocumentLink=""
    if(d['doableType']=='compliance'):
        relatedDocumentLink=""   #update link of document if any

    data={
        "senderId": d['assignedBy'],
        "receiverId": d['assignedTo'],
        "messageType": "doable",
        "messageContent": d["subject"],
        "relatedDocumentLink":relatedDocumentLink,
        "doableId": str(d['doableId']),
        "doableType": d['doableType']
    }

    try:
        response = create_message(data)
        print("response",response)
        
        if response=='New Message Created':
            #serializer.save()
            print("doable created")
            return JsonResponse({"message":"doable created and assigned", "success":True}, status=200, safe=False)
        else:
            print("doable not created Please try again")
            return JsonResponse({"message":response, "success":False}, status=200, safe=False)
        
    except:
        #print(e)
        #print("doable not created Please try again")
        return JsonResponse({"message":"message not send", "success":False}, status=200, safe=False)



        #return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    # print(serializer.errors)
    # return HttpResponse(content='doable not created Please try again'+str(serializer.errors), status=200)




@api_view(['GET'])
def allCompliancePage(request):
    user_id=request.user.id
    page1=request.GET.get('page1')
    page2=request.GET.get('page2')
    limit=10
    d=Profile.objects.get(pk=user_id)
    out={}
    sql_assigned_by="""
        select * from doables_doable d  left join auth_user u on d."assignedTo"=u."id" where "assignedBy"=%s;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_assigned_by,[user_id])
        row=dictfetchall(cursor)
    paginator=Paginator(row,limit)
    try:
        content = paginator.page(page1).object_list
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        content = paginator.page(1).object_list
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages).object_list
    out['assignedBy']=content
    #print(row)
    # for i in out["assignedBy"]:
    #     # print(i["assignedTo"])
    #     u=User.objects.get(pk=i["assignedTo"])
    #     i["assignedToUser"]={"first_name":u.first_name, "last_name":u.last_name}

    sql_assigned_to="""
        select * from doables_doable d left join auth_user u on d."assignedBy"=u."id" where "assignedTo"=%s;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_assigned_to,[user_id])
        row=dictfetchall(cursor)
    paginator=Paginator(row,limit)
    try:
        content = paginator.page(page2).object_list
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        content = paginator.page(1).object_list
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages).object_list
    out['assignedTo']=content
    #print(row)
    return JsonResponse(out,status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
def getComplianceDetail(request):
    id= request.GET.get('doableId')
    page=request.GET.get('page')
    limit=5  #content on a page

    sql="""
    select u1."first_name"  as sender_first_name, u1."last_name" as sender_last_name, u1."id" as sender_id ,u2."first_name"  as receiver_first_name, u2."last_name" as receiver_last_name, u2."id" as receiver_id , "messageId", "messageType","messageContent","relatedDocumentLink","timestampCreation"
    from message_message m 
    inner join auth_user u1 on u1."id"=m."senderId"
    inner join auth_user u2 on u2."id"=m."receiverId" where "doableId"=%s;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql,[id])
        row=dictfetchall(cursor)
    paginator=Paginator(row,limit)


    try:
        content = paginator.page(page).object_list
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        content = paginator.page(1).object_list
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages).object_list


    return JsonResponse(content,status=status.HTTP_200_OK, safe=False)

@api_view(['PUT'])
def updateDoable(request):
    d= JSONParser().parse(request)
    id=d['doableId']
    d.pop('doableId')
    try:
        doable.objects.filter(pk=id).update(**d)
    except IntegrityError as execption:
        print(str(execption))
        return HttpResponseBadRequest("Integrity error")
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to Update group: Try Again")
    return HttpResponse("doable Updated")
        
@api_view(['DELETE'])
def deleteDoable(request):
    id=request.GET.get('doableId')
    doableId=id
    try:
        message.objects.filter(doableId=doableId).delete()
        doable.objects.get(pk=doableId).delete()
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to delete : Try Again")
    return HttpResponse("Doable deleted")