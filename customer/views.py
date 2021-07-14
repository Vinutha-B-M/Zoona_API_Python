from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

import datetime
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerInfoSerializer, VehicleInfoSerializer, TestDetailsSerializer
from .models import CustomerInfo, VehicleInfo, TestDetails
from rest_framework import viewsets, status


class Customer_List(APIView):

    def get(self, request):
        cust1 = CustomerInfo.objects.all()
        today = datetime.datetime.now()
        cust2 = CustomerInfo.objects.filter(created_date__year=today.year, created_date__month=today.month)
        total_number = cust1.count()
        new_number = cust2.count()
        customer_count= {"total_count":total_number, "new_count":new_number}
        # serializer1 = CustomerInfoSerializer(cust1, many=True)
        return JsonResponse(customer_count,safe=False)

    def post(self, request):
        data = request.data
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
        if CustomerInfo.objects.filter(phone_number=phone_number).exists():
                myJson = {"status": "0", "message": "Phone Number Exits"}
                return JsonResponse(myJson)
        else:
                create = CustomerInfo.objects.create(company_name=company_name, full_name=full_name, email_id=email_id,
                                                    address=address,postal_code=postal_code, selected_date=selected_date,
                                                    phone_number=phone_number,address_2=address_2,city=city,state=state)
                serializer3 = CustomerInfoSerializer(create)
                return Response(serializer3.data)


class Vehicle_List(APIView):

    def get(self, request):
        cust2 = VehicleInfo.objects.all()
        serializer = VehicleInfoSerializer(cust2, many=True)
        return Response(serializer.data)

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
        customer_obj = CustomerInfo.objects.get(id=customer_id)
        create = VehicleInfo.objects.create(customer_id=customer_obj, year=year, brand=brand, brand_model=brand_model,
                                            odo_meter=odo_meter, lic_plate=lic_plate, gvwr=gvwr, vin=vin, engine=engine,
                                            cylinder=cylinder,Transmission=Transmission)
        serializer3 = VehicleInfoSerializer(create)
        return Response(serializer3.data)


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
    return JsonResponse("WELCOME",safe=False)


class month_count(APIView):

    def get(self, request):
        today = datetime.datetime.now()
        cust2 = CustomerInfo.objects.filter(created_date__year=today.year,created_date__month=today.month)
        total_number = cust2.count()

        return JsonResponse(total_number,safe=False)


class vehicle_info(APIView):

    def post(self, request):
        data = request.data
        vinField = data['vinField']
        response = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/'+vinField+'?format=json')
        json_response = response.json()
        return JsonResponse(json_response, safe=False)