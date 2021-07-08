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
            return JsonResponse({'status': 'UserName is Already Exits'})
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
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'Password is not Correct'})
        else:
            return JsonResponse({'status': 'UserName Doesnot Exits'})


class forgot(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        if UserInfo.objects.filter(username=username).exists():
            return JsonResponse({'status': 'User Exits'})
        else:
            return JsonResponse({'status': 'UserName is Doesnot Exits'})


class update(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        if UserInfo.objects.filter(username=username).exists():
            cust_obj = UserInfo.objects.filter(username=username).update(password=password)
            return JsonResponse({'status': 'password Updated'})
        else:
            return JsonResponse({'status': 'UserName is Doesnot Exits'})


class user_info(APIView):

    def post(self, request):
        data = request.data
        id = data['user_id']
        if UserInfo.objects.filter(id=id).exists():
            user_obj = UserInfo.objects.get(id=id)
            serializer = UserInfoSerializer(user_obj)
            return Response(serializer.data)
        else:
            return JsonResponse({'status': 'UserName is Doesnot Exits'})