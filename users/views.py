from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserInfoSerializer
from .models import UserInfo
from rest_framework import viewsets, status


class signup(APIView):

    def post(self, request):
        data = request.data
        full_name = data['full_name']
        username = data['username']
        password = data['password']
        if UserInfo.objects.filter(username=username).exists():
            myJson = {"status": "0", "message": "Username Exits"}
            return JsonResponse(myJson)
        else:
            create = UserInfo.objects.create(full_name=full_name, username=username, password=password)
            serializer = UserInfoSerializer(create)
            return Response(serializer.data)


class login(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        if UserInfo.objects.filter(username=username).exists():
                if UserInfo.objects.get(username=username).password == password:
                    request.session['user_id'] = UserInfo.objects.get(username=username).id
                    myJson = {"status": "1", "message": "Success"}
                    return JsonResponse(myJson)
                else:
                    myJson = {"status": "0", "message": "Password is not Correct"}
                    return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "UserName Doesnot Exits"}
            return JsonResponse(myJson)


class forgot(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        if UserInfo.objects.filter(username=username).exists():
            myJson = {"status": "1", "message": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "UserName Doesnot Exits"}
            return JsonResponse(myJson)


class update(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        if UserInfo.objects.filter(username=username).exists():
            cust_obj = UserInfo.objects.filter(username=username).update(password=password)
            myJson = {"status": "1", "message": "Success"}
        else:
            myJson = {"status": "0", "message": "UserName Doesnot Exits"}
            return JsonResponse(myJson)


class user_info(APIView):

    def post(self, request):
        data = request.data
        id = data['user_id']
        if UserInfo.objects.filter(id=id).exists():
            user_obj = UserInfo.objects.get(id=id)
            serializer = UserInfoSerializer(user_obj)
            return Response(serializer.data)
        else:
            myJson = {"status": "0", "message": "UserName Doesnot Exits"}
            return JsonResponse(myJson)