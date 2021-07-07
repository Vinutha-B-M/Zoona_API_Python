from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
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
        serializer1 = CustomerInfoSerializer(cust1, many=True)
        return Response(serializer1.data)

    def post(self, request):
        serializer = CustomerInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        customer_obj = CustomerInfo.objects.get(id=customer_id)
        create = VehicleInfo.objects.create(customer_id=customer_obj, year=year, brand=brand, brand_model=brand_model,
                                            odo_meter=odo_meter, lic_plate=lic_plate, gvwr=gvwr, vin=vin, engine=engine,
                                            cylinder=cylinder)
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