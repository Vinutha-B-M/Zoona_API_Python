from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
import json
import random, string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserInfoSerializer, UserTypeSerializer
from .models import UserInfo, UserType
from rest_framework import viewsets, status
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class signup(APIView):

    def post(self, request):
        data = request.data
        company_name = data['company_name']
        full_name = data['full_name']
        username = data['username']
        username = username.lower()
        password = data['password']
        if UserType.objects.filter(username=username).exists():
            myJson = {"status": "0", "data": "Username Exits"}
            return JsonResponse(myJson)
        else:

            create_obj = UserInfo.objects.create(company_name=company_name)
            create = UserType.objects.create(full_name=full_name, username=username, password=password,
                                             userinfo=create_obj, is_admin=True)
            serializer = UserTypeSerializer(create)
            html_content = render_to_string('signup.html', {'full_name': full_name,'username':username,'password':password})  # render with dynamic value
            text_content = strip_tags(html_content)
            email_subject = f'AutoPos Admin Account For Zunaco'
            # message = f"Hi {full_name}, \n\n"\
            #           f"Zunaco welcomes you on board, refer the below mentioned credentials to login to your application.  \n\n" \
            #           f"Login ID/UserName: {username} \n"\
            #           f"Password: {password} \n\n"\
            #           f"Regards, \nTeam AutoPos"
            from_mail = settings.EMAIL_HOST_USER
            to_list = [username]
            msg = EmailMultiAlternatives(email_subject, text_content, from_mail, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # send_mail(email_subject, message, from_mail, to_list, fail_silently=False)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)


class login(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        username = username.lower()
        password = data['password']
        if UserType.objects.filter(username=username).exists():
            if UserType.objects.get(username=username).password == password:
                request.session['user_id'] = UserType.objects.get(username=username).id
                user_id = UserType.objects.get(username=username).id
                user_obj = UserType.objects.get(id=user_id)
                serializer = UserTypeSerializer(user_obj)
                myJson = {"status": "1", "data": serializer.data}
                return JsonResponse(myJson)
            else:
                myJson = {"status": "0", "data": "Password is not Correct"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "UserName Does not Exits"}
            return JsonResponse(myJson)


class forgot(APIView):

    def post(self, request):
        data = request.data
        username = data['username']
        username = username.lower()
        if UserType.objects.filter(username=username).exists():
            allowed_chars = ''.join((string.ascii_letters, string.digits))
            unique_id = ''.join(random.choice(allowed_chars) for _ in range(12))
            html_content = render_to_string('forgot.html', { 'username': username,
                                                            'password': unique_id})  # render with dynamic value
            text_content = strip_tags(html_content)
            email_subject = f'Your Password Changed <> AutoPos'

            from_mail = settings.EMAIL_HOST_USER
            to_list = [username]
            msg = EmailMultiAlternatives(email_subject, text_content, from_mail, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            UserType.objects.filter(username=username).update(password=unique_id)
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "UserName Does not Exits"}
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
                myJson = {"status": "1", "data": "Success"}
                return JsonResponse(myJson)
            else:
                myJson = {"status": "0", "data": "Password is Wrong"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "UserName Does not Exits"}
            return JsonResponse(myJson)


class user_info(APIView):

    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']

        if UserType.objects.filter(id=session).exists():
            user_obj = UserType.objects.get(id=session)
            serializer = UserTypeSerializer(user_obj)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "UserName Does not Exits"}
            return JsonResponse(myJson)


class update_user_info(APIView):
    def post(self, request):

        data = request.data
        pic = request.FILES.get('profile')
        session = data['id']
        full_name = data['full_name']
        username = data['username']
        username = username.lower()
        phone_number = data['phone_number']
        company_name = data['company_name']

        if UserType.objects.filter(id=session).exists():

            user_obj = UserType.objects.get(id=session)
            user = UserInfo.objects.get(id=user_obj.userinfo.id)
            user.company_name = company_name
            user.save()
            user_obj.full_name=full_name
            user_obj.username=username
            user_obj.phone_number=phone_number
            if pic != None:
                user_obj.profile=pic
                user_obj.image_name=pic
            user_obj.save()
            user_data = UserType.objects.get(id=session)
            serializer = UserTypeSerializer(user_data)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "UserName Does not Exits"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class add_user(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        username = data['username']
        username = username.lower()
        is_admin = data['is_admin']
        company_name = user_obj.company_name
        allowed_chars = ''.join((string.ascii_letters, string.digits))
        unique_id = ''.join(random.choice(allowed_chars) for _ in range(12))
        if UserType.objects.filter(username=username).exists():
            myJson = {"status": "0", "data": "Username Exits"}
            return JsonResponse(myJson)
        else:
            user_obj = UserType.objects.create(username=username, is_admin=is_admin, password=unique_id,
                                               userinfo=user_obj)
            email_subject = f'Your Zunaco AutoPos Account  For {company_name}'
            html_content = render_to_string('new_user.html', { 'username': username,
                                                            'password': unique_id})  # render with dynamic value
            text_content = strip_tags(html_content)
            from_mail = settings.EMAIL_HOST_USER
            to_list = [username]
            msg = EmailMultiAlternatives(email_subject, text_content, from_mail, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            myJson = {"status": "1", "data": "success"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class users_data(APIView):

    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']

        if UserType.objects.filter(id=session, is_admin=True).exists():
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            user_data = UserType.objects.filter(userinfo=user_obj)
            serializer = UserTypeSerializer(user_data, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)


class update_users(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['user_id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        username = data['username']
        username = username.lower()
        is_admin = data['is_admin']
        if UserType.objects.filter(username=username).exists():
            myJson = {"status": "0", "data": "UserName Exits"}
            return JsonResponse(myJson)
        else:
            user_obj = UserType.objects.filter(id=session).update(username=username, is_admin=is_admin)
            myJson = {"status": "1", "data": "success"}
            return JsonResponse(myJson)


class delete_users(APIView):
    def post(self, request):
        data = request.data
        session = data['user_id']
        if UserType.objects.filter(id=session).exists():
            user_obj = UserType.objects.get(id=session).delete()
            myJson = {"status": "1", "data": "success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)


@csrf_exempt
def company_logo(request):
    if request.method == 'POST':
        pic=request.FILES.get('company_logo')
        id = request.POST.get('id')
        if UserType.objects.filter(id=id).exists():
            user_info_obj = UserType.objects.get(id=id)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            user_profile=UserInfo.objects.get(id=user_obj.id)
            user_profile.company_logo=pic
            user_profile.save()
            user_data = UserType.objects.filter(userinfo=user_obj)
            serializer = UserTypeSerializer(user_data, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data":"error"}
            return JsonResponse(myJson)