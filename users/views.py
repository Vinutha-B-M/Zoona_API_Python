from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
import json
import random,string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserInfoSerializer,UserTypeSerializer
from .models import UserInfo,UserType
from rest_framework import viewsets, status
from django.conf import settings
from django.core.mail import send_mail

class signup(APIView):

    def post(self, request):
        data = request.data
        company_name = data['company_name']
        full_name = data['full_name']
        username = data['username']
        password = data['password']
        if UserType.objects.filter(username=username).exists():
            myJson = {"status": "0", "message": "Username Exits"}
            return JsonResponse(myJson)
        else:

            create_obj = UserInfo.objects.create(company_name=company_name)
            create = UserType.objects.create(full_name=full_name, username=username, password=password,
                                             userinfo=create_obj,is_admin=True)
            serializer = UserTypeSerializer(create)
            return Response(serializer.data)


class login(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        if UserType.objects.filter(username=username).exists():
                if UserType.objects.get(username=username).password == password:
                    request.session['user_id'] = UserType.objects.get(username=username).id
                    user_id = UserType.objects.get(username=username).id
                    user_obj= UserType.objects.get(id=user_id)
                    serializer = UserTypeSerializer(user_obj)
                    return Response(serializer.data)

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
        if UserType.objects.filter(username=username).exists():
            myJson = {"status": "1", "message": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "UserName Doesnot Exits"}
            return JsonResponse(myJson)


class update(APIView):

    def post(self, request):
        data = request.data
        id = data['id']
        old_password = data['old_password']
        password = data['new_password']
        if UserType.objects.filter(id=id).exists():
            if UserType.objects.get(id=id).password == old_password:
                 cust_obj = UserType.objects.filter(id=id).update(password=password)
                 myJson = {"status": "1", "message": "Success"}
                 return JsonResponse(myJson)
            else:
                myJson = {"status": "0", "message": "Password is Wrong"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "User Doesnot Exits"}
            return JsonResponse(myJson)


class user_info(APIView):

    def get(self, request):
        session = request.session.get("user_id")
        if session:
            if UserType.objects.filter(id=session).exists():
                user_obj = UserType.objects.get(id=session)
                serializer = UserTypeSerializer(user_obj)
                return Response(serializer.data)
            else:
                myJson = {"status": "0", "message": "UserName Doesnot Exits"}
                return JsonResponse(myJson)

    def post(self, request):
        session = request.session.get("user_id")
        if session:
            data = request.data
            full_name = data['full_name']
            username = data['username']
            phone_number = data['phone_number']
            if UserType.objects.filter(id=session).exists():

                user_obj = UserType.objects.filter(id=session).update(full_name=full_name, username=username,
                                                                      phone_number=phone_number)
                user_data = UserType.objects.get(id=session)
                serializer = UserTypeSerializer(user_data)
                return Response(serializer.data)
            else:
                myJson = {"status": "0", "message": "UserName Doesnot Exits"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)


class add_user(APIView):
    def post(self,request):
        session = request.session.get("user_id")
        if session:
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            data = request.data
            username = data['username']
            company_name = user_obj.company_name
            allowed_chars = ''.join((string.ascii_letters, string.digits))
            unique_id = ''.join(random.choice(allowed_chars) for _ in range(32))
            user_obj=UserType.objects.create(username=username,is_admin=False,company_name=company_name,
                                             password=unique_id,userinfo=user_obj)
            email_subject = f'Your Sales Account  For {company_name}'
            message = f"Your Username is<b> {username}</b> with Password :<b> {unique_id} </b>\n" \
                      f"Don't share your details with others"
            from_mail = settings.EMAIL_HOST_USER
            to_list = [username]
            send_mail(email_subject, message, from_mail, to_list, fail_silently=False)
            myJson = {"status": "1", "message": "User Created"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)

