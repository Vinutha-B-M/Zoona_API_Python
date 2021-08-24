from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

import datetime
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerInfoSerializer, VehicleInfoSerializer, TestDetailsSerializer,TermsItemSerializer
from .models import CustomerInfo, VehicleInfo, TestDetails,TermsItems
from service.models import TermCondition
from users.models import UserInfo, UserType
from rest_framework import viewsets, status
from payment.models import PaymentEntry, InvoiceItem
from django.core import serializers

class Customer_List(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_id = session
        user_info_obj = UserType.objects.get(id=user_id)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        cust1 = CustomerInfo.objects.filter(user_id=user_obj)
        today = datetime.datetime.now()
        cust2 = CustomerInfo.objects.filter(created_date__year=today.year, created_date__month=today.month,
                                            user_id=user_obj)
        cust3 = VehicleInfo.objects.filter(customer_id__in=cust1)
        payment = PaymentEntry.objects.filter(Vehicle__in=cust3)
        total_number = cust1.count()
        new_number = cust2.count()
        customer_count = {"total_count": total_number, "new_count": new_number}
        # serializer1 = CustomerInfoSerializer(cust1, many=True)
        return JsonResponse(customer_count, safe=False)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)
class fetch_customer_info(APIView):
    def post(self,request):
        data = request.data
        session = data['id']
        phone_number = data['phone_number']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if CustomerInfo.objects.filter(phone_number=phone_number,user_id=user_obj).exists():
            obj=CustomerInfo.objects.get(phone_number=phone_number)
            serializer = CustomerInfoSerializer(obj)
            termitems = TermsItems.objects.filter(customer=obj)
            serializer2 = TermsItemSerializer(termitems)
            myJson = {"status": "1", "data": serializer.data,"terms":serializer2.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": ''}
            return JsonResponse(myJson)

class add_Customer_List(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        company_name = data['company_name']
        full_name = data['full_name']
        email_id = data['email_id']
        address = data['address']
        address_2 = data['address_2']
        city = data['city']
        state = data['state']
        phone_number = data['phone_number']
        postal_code = data['postal_code']
        selected_date = data['selected_date']
        terms_item = data['terms_item']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if CustomerInfo.objects.filter(phone_number=phone_number,user_id=user_obj).exists():
            myJson = {"status": "0", "data": "Phone Number Exits"}
            return JsonResponse(myJson)
        else:
            create = CustomerInfo.objects.create(company_name=company_name, full_name=full_name, email_id=email_id,
                                                 address=address, postal_code=postal_code, selected_date=selected_date,
                                                 phone_number=phone_number, address_2=address_2, city=city, state=state,
                                                 user_id=user_obj)
            for i in terms_item:
                tax_id = i['id']
                term_obj = TermCondition.objects.get(id=tax_id)
                term_text = TermCondition.objects.get(id=tax_id).term_text
                TermsItems.objects.create(terms_text=term_text,term=term_obj,customer=create)
            serializer = CustomerInfoSerializer(create)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)


def term_item_updation(customer_exist, terms_item):
    for i in terms_item:
        tax_id = i['id']
        tax_obj = TermCondition.objects.get(id=tax_id)
        term_text = TermCondition.objects.get(id=tax_id).term_text
        if TermsItems.objects.filter(term=tax_id, customer=customer_exist):
            TermsItems.objects.filter(term=tax_id).update(terms_text=term_text)
        else:
            TermsItems.objects.create(term=tax_obj, terms_text=term_text, customer=customer_exist)

    updated_list = TermsItems.objects.filter(customer=customer_exist).values_list('term',flat=True)

    for i in updated_list:
        dt = 0
        for j in terms_item:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
                TermsItems.objects.filter(term=i,customer=customer_exist).delete()


class update_customer_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        company_name = data['company_name']
        full_name = data['full_name']
        email_id = data['email_id']
        address = data['address']
        address_2 = data['address_2']
        city = data['city']
        state = data['state']
        phone_number = data['phone_number']
        postal_code = data['postal_code']
        selected_date = data['selected_date']
        terms_item = data['terms_item']
        customer_exist=CustomerInfo.objects.get(id=session)
        CustomerInfo.objects.filter(id=session).update(company_name=company_name, full_name=full_name,
                                                             email_id=email_id,address=address, postal_code=postal_code,
                                                             selected_date=selected_date,
                                                             phone_number=phone_number, address_2=address_2, city=city,
                                                             state=state)
        none_response=term_item_updation(customer_exist,terms_item)
        create=CustomerInfo.objects.get(id=session)
        serializer = CustomerInfoSerializer(create)
        myJson = {"status": "1", "data": serializer.data}
        return JsonResponse(myJson)


class Vehicle_List(APIView):

    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        serializer = VehicleInfoSerializer(cust2, many=True)
        SomeModel_json = serializers.serialize("json", cust2)
        # customer_obj = CustomerInfo.objects.filter(user_id=user_obj).exclude(id__in=cust2.customer_id[id])
        serializer2 = CustomerInfoSerializer(customer_obj, many=True)
        myJson = {"status": "1", "vehicle_info": serializer.data, "customer_info": serializer2.data}
        return JsonResponse(myJson)


class add_Vehicle_List(APIView):
    def post(self, request):
        data = request.data
        year = data['year']
        brand = data['brand']
        brand_model = data['brand_model']
        odo_meter = data['odo_meter']
        lic_plate = data['lic_plate']
        gvwr = data['gvwr']
        vin = data['vin']
        engine = data['engine']
        cylinder = data['cylinder']
        customer_id = data['customer_id']
        Transmission = data['Transmission']
        engine_group = data['engine_group']
        customer_obj = CustomerInfo.objects.get(id=customer_id)
        user = UserInfo.objects.get(id=customer_obj.user_id.id).id
        user_obj = UserInfo.objects.get(id=user)
        customer_obj_list = CustomerInfo.objects.filter(user_id=user_obj)
        if CustomerInfo.objects.filter(user_id=user).exists():
            if VehicleInfo.objects.filter(customer_id__in=customer_obj_list,vin=vin).exists():
                myJson = {"status": "0", "data": "VIN Exists"}
                return JsonResponse(myJson)
            else:
                create = VehicleInfo.objects.create(customer_id=customer_obj, year=year, brand=brand,
                                                    brand_model=brand_model,
                                                    odo_meter=odo_meter, lic_plate=lic_plate, gvwr=gvwr, vin=vin,
                                                    engine=engine,
                                                    cylinder=cylinder, Transmission=Transmission,
                                                    engine_group=engine_group)
                serializer = VehicleInfoSerializer(create)
                myJson = {"status": "1", "data": serializer.data}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data":"login_error"}
            return JsonResponse(myJson)

class update_vehicle_list(APIView):
    def post(self, request):
        data = request.data
        year = data['year']
        brand = data['brand']
        brand_model = data['brand_model']
        odo_meter = data['odo_meter']
        lic_plate = data['lic_plate']
        gvwr = data['gvwr']
        vin = data['vin']
        engine = data['engine']
        cylinder = data['cylinder']
        vehicle_id = data['id']
        Transmission = data['Transmission']
        engine_group = data['engine_group']
        vehicle = VehicleInfo.objects.get(id=vehicle_id)
        customer = CustomerInfo.objects.get(id=vehicle.customer_id.id).id
        if VehicleInfo.objects.filter(id=vehicle_id).exists():
            customer_obj = CustomerInfo.objects.get(id=customer)
            user = UserInfo.objects.get(id=customer_obj.user_id.id).id
            user_obj = UserInfo.objects.get(id=user)
            customer_obj_list = CustomerInfo.objects.filter(user_id=user_obj).values_list('id')
            if CustomerInfo.objects.filter(user_id=user,id=customer).exists():
                if VehicleInfo.objects.filter(customer_id=customer_obj,vin=vin,id=vehicle_id).exists():
                    VehicleInfo.objects.filter(id=vehicle_id).update(year=year, brand=brand, brand_model=brand_model,
                                                                     odo_meter=odo_meter, lic_plate=lic_plate, gvwr=gvwr,
                                                                     vin=vin, engine=engine,
                                                                     cylinder=cylinder, Transmission=Transmission,
                                                                     engine_group=engine_group)
                    create = VehicleInfo.objects.get(id=vehicle_id)
                    serializer = VehicleInfoSerializer(create)
                    myJson = {"status": "1", "data": serializer.data}
                    return JsonResponse(myJson)
                elif VehicleInfo.objects.filter(customer_id__in=customer_obj_list,vin=vin).exists():
                    myJson = {"status": "0", "data": "VIN Exists"}
                    return JsonResponse(myJson)
                else:
                    VehicleInfo.objects.filter(id=vehicle_id).update(year=year, brand=brand, brand_model=brand_model,
                                                                     odo_meter=odo_meter, lic_plate=lic_plate,
                                                                     gvwr=gvwr,
                                                                     vin=vin, engine=engine,
                                                                     cylinder=cylinder, Transmission=Transmission,
                                                                     engine_group=engine_group)
                    create = VehicleInfo.objects.get(id=vehicle_id)
                    serializer = VehicleInfoSerializer(create)
                    myJson = {"status": "1", "data": serializer.data}
                    return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": "Login_error"}
            return JsonResponse(myJson)

class Test_List(APIView):

    def get(self, request):
        cust2 = TestDetails.objects.all()
        serializer = TestDetailsSerializer(cust2, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        selected_date = data['selected_date']
        vehicle_id = data['vehicle_id']
        vehicle_obj = VehicleInfo.objects.get(id=vehicle_id)
        create = TestDetails.objects.create(vehicle_id=vehicle_obj, selected_date=selected_date)
        serializer = TestDetailsSerializer(create)
        return Response(serializer.data)


def home(request):
    return JsonResponse("WELCOME", safe=False)


class vehicle_info(APIView):

    def post(self, request):
        data = request.data
        vinField = data['vinField']
        response = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/' + vinField + '?format=json')
        json_response = response.json()
        return JsonResponse(json_response, safe=False)
