from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import ReceiptContentSerializer, TaxesSerializer, DiscountsSerializer, ServiceListSerializer,DefaultListSerializer
from .models import ReceiptContent, Taxes, Discounts, ServicesList,Default
from django.http import HttpResponse, JsonResponse
from users.models import UserInfo, UserType


# Create your views here.
class receipt_content(APIView):
    def get(self,request):
        session = request.session.get("user_id")
        if session:
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if ReceiptContent.objects.filter(client=user_obj).exists():
                content = ReceiptContent.objects.get(client=user_obj)
                obj=ReceiptContentSerializer(content)
                return Response(obj.data)
            else:
                myJson = {"status": "1", "message": "no data"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)

    def post(self, request):
        session = request.session.get("user_id")
        if session:
            data = request.data
            company_name = data['company_name']
            address = data['address']
            phone_number = data['phone_number']
            website_url = data['website_url']
            footer_note = data['footer_note']
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)

            if UserType.objects.filter(id=session,is_admin=True).exists():
                create = ReceiptContent.objects.create(company_name=company_name, address=address,phone_number=phone_number,
                                                       website_url=website_url, footer_note=footer_note, client=user_obj)
                serializer = ReceiptContentSerializer(create)
                return Response(serializer.data)

            else:
                myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)


class discounts(APIView):

    def get(self, request):
        session = request.session.get("user_id")
        if session:
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if Discounts.objects.filter(client=user_obj).exists():
                content = Discounts.objects.filter(client=user_obj)
                obj = DiscountsSerializer(content,many=True)
                return Response(obj.data)
            else:
                myJson = {"status": "1", "message": "no data"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)

    def post(self, request):
        session = request.session.get("user_id")
        if session:
            data = request.data
            discount_value = data['discount_value']
            offer_name = data['offer_name']
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if UserType.objects.filter(id=session,is_admin=True).exists():
                create = Discounts.objects.create(discount_value=discount_value, offer_name=offer_name, client=user_obj)
                serializer = DiscountsSerializer(create)
                return Response(serializer.data)
            else:
                myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)


class taxes(APIView):
    def get(self, request):
        session = request.session.get("user_id")
        if session:
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if Taxes.objects.filter(client=user_obj).exists():
                content = Taxes.objects.filter(client=user_obj)
                obj = TaxesSerializer(content, many=True)
                return Response(obj.data)
            else:
                myJson = {"status": "1", "message": "no data"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)

    def post(self, request):
        session = request.session.get("user_id")
        if session:
            data = request.data
            tax_value = data['tax_value']
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if UserType.objects.filter(id=session,is_admin=True).exists():
                create = Taxes.objects.create(tax_value=tax_value, client=user_obj)
                serializer = TaxesSerializer(create)
                return Response(serializer.data)
            else:
                myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)


class services(APIView):
    def get(self, request):
        session = request.session.get("user_id")
        if session:
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if ServicesList.objects.filter(client=user_obj).exists():
                content = ServicesList.objects.filter(client=user_obj)
                obj = ServiceListSerializer(content, many=True)
                return Response(obj.data)
            else:
                myJson = {"status": "1", "message": "no data"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)


    def post(self, request):
        session = request.session.get("user_id")
        if session:
            data = request.data
            service_name = data['service_name']
            input_mode = data['input_mode']
            amount = data['amount']
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)

            if UserType.objects.filter(id=session,is_admin=True).exists():
                create = ServicesList.objects.create(service_name=service_name, input_mode=input_mode,
                                                     client=user_obj, amount=amount)
                serializer = ServiceListSerializer(create)
                return Response(serializer.data)
            else:
                myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)


class defaults(APIView):
    def get(self,request):
        session = request.session.get("user_id")
        if session:
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if Default.objects.filter(client=user_obj).exists():
                content = Default.objects.get(client=user_obj)
                obj=DefaultListSerializer(content)
                return Response(obj.data)
            else:
                myJson = {"status": "1", "message": "no data"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)

    def post(self, request):
        session = request.session.get("user_id")
        if session:
            data = request.data
            currency = data['currency']
            langaugge = data['langaugge']
            time_zone = data['time_zone']
            display_time = data['display_time']
            date_format = data['date_format']
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            if UserType.objects.filter(id=session,is_admin=True).exists():
                create = Default.objects.create(currency=currency, langaugge=langaugge,time_zone=time_zone,
                                                display_time=display_time, date_format=date_format,client=user_obj)
                serializer = DefaultListSerializer(create)
                return Response(serializer.data)

            else:
                myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "Login expired"}
            return JsonResponse(myJson)
