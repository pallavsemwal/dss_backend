from datetime import datetime
from http.client import HTTPResponse
from telnetlib import STATUS
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse,HttpResponseBadRequest, HttpResponseServerError, FileResponse, HttpRequest
import json
from details.models.profile import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.core import serializers
from message.serializer import messageSerializer
from message.tokenId import token
from message.models import message
from django.db import IntegrityError
from requests import Session
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from doables.models import doable

def send_notice(TO,noticeLink,committeeName,scheduledDate):
    BASE_URL = "https://graph.facebook.com/"
    API_VERSION = "v14.0/"
    SENDER = "107663142104977/"
    ENDPOINT = "messages"
    URL = BASE_URL + API_VERSION + SENDER + ENDPOINT
    API_TOKEN = token
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    parameters = {
        "messaging_product": "whatsapp",
        "to": TO,
        "type": "template",
        "template": {
            "name": "notice_alert",
            "language": {
                "code": "en"
            },
            "components":[
                {
                    "type":"header",
                    "parameters": [
                        {
                            "type": "document",
                            "document":{
                                "link": noticeLink
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": committeeName
                        },
                        {
                            "type": "text",
                            "text": scheduledDate
                        }
                        
                    ]
                }
            ]
        }
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.post(URL, json=parameters)
        data = json.loads(response.text)
        print(f"data: {data}")
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return False


def send_doable(TO,target_type,target):
    BASE_URL = "https://graph.facebook.com/"
    API_VERSION = "v14.0/"
    SENDER = "107663142104977/"
    ENDPOINT = "messages"
    URL = BASE_URL + API_VERSION + SENDER + ENDPOINT
    API_TOKEN = token
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    parameters = {
        "messaging_product": "whatsapp",
        "to": TO,
        "type": "template",
        "template": {
            "name": "target_alert",
            "language": {
                "code": "en"
            },
            "components":[
                
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": target_type
                        },
                        {
                            "type": "text",
                            "text": target
                        }
                        
                    ]
                }
            ]
        }
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.post(URL, json=parameters)
        data = json.loads(response.text)
        print(f"data: {data}")
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return False




def create_message(data):
     #data should contain senderId, receiverId, messageType, messageContent, relatedDocumentLink,doableId
                                         #committeeName,scheduledDate
    print(data)
    receiver=json.loads(serializers.serialize('json',Profile.objects.filter(pk=data["receiverId"])))
    
    TO=receiver[0]["fields"]["mobileNumber"] #receiver mobile number
    
    message_type=data['messageType']
    
    if message_type=='notice':
        committee_name=data["committeeName"]    
        scheduledDate=data["scheduledDate"]
        out_data=send_notice(TO,data['relatedDocumentLink'],committee_name,scheduledDate)
        print(1)
    if message_type=="doable":
        doable_type=data['doableType']
        out_data=send_doable(TO,doable_type,data['messageContent'])
        #print("1")
    if out_data==False:
        return "Something went wrong in creating message. Please try after sometime"
    if 'error' in out_data:
        print('error in creating message: '+out_data['error']['message'])
        return out_data['error']['message']
    else:
        #print(out_data)
        waMessageId=out_data['messages'][0]['id']
        #print(out_data)
        print("waMessageID", waMessageId)
        print(data['senderId'])
        print(data['receiverId'])
        print(data['messageType'])
        print(data['relatedDocumentLink'])
        print("2022-10-13 11:00:00")
        #print(data['doableId'])
        print(2)
        save_data={}

        save_data['messageId']=waMessageId;
        save_data['senderId']=data['senderId']
        save_data['receiverId']=data['receiverId']
        save_data['messageType']=data['messageType']
        save_data['messageContent']=""
        save_data['relatedDocumentLink']=data['relatedDocumentLink']
        save_data['timestampCreation']=datetime.now()
        print(3)

        if 'doableId' in data:
            save_data['doableId']=data['doableId']
            save_data['messageContent']=data['messageContent']
        try:
            message.objects.create(**save_data)
            print(4)
        except IntegrityError as execption:
            print(str(execption))
            return "Integrity error in message"
            print(5)
        except Exception as exception:
            print(str(exception))
            return "Failed to create message: Try Again"
            print(6)
        return "New Message Created"




        #serializer = messageSerializer(data=save_data)
        #if(serializer.is_valid()):
           # serializer.save()
            #print(serializer.data)
            #return HTTPResponse(content="Message Created All good")
        #print(serializer.errors)

        # data['messageId']=id
        # data['timestampCreation']=datetime.datetime.now()
        # serializer = messageSerializer(data=data)
        # if(serializer.is_valid()):
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        #return HttpResponse(content='', status=200)
        
    



