from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from customer.models import CustomerInfo, VehicleInfo, TestDetails
from .models import PaymentEntry, InvoiceItem
from service.models import ServicesList
from .serializers import PaymentEntrySerializer,InvoiceItemSerializer

# class device_list(APIView):
#
#     def get(self, request):
#         response = requests.get('https://connect.squareupsandbox.com/v2/locations/L8BKETKRHE1PP/transactions/',
#                                 headers={"Authorization": "Bearer EAAAENz618Mx91J_aZ2jq-VAlBEr05uLz6yTMngy84AfbuBCvKAvQ38pyhNKLYT3"})
#         json_response = response.json()
#         return JsonResponse(json_response)
#
#     def post(self, request):
#
#       return

class payment_entry(APIView):
    def post(self, request):
        data = request.data
        final_amount = data['final_amount']
        tax_offered = data['tax_offered']
        discount_offered = data['discount_offered']
        status = data['status']
        vehicle = data['Vehicle_id']
        payment_mode = 'Cash'
        vehicle_obj=VehicleInfo.objects.get(id=vehicle)
        service_item = data['service_item']
        payment_obj = PaymentEntry.objects.create(final_amount=final_amount, tax_offered=tax_offered,
                                                  discount_offered=discount_offered,payment_mode=payment_mode,
                                                  status=status, Vehicle=vehicle_obj)
        for i in service_item:
            service_id = i['id']
            service_obj = ServicesList.objects.get(id=service_id)
            service_name = ServicesList.objects.get(id=service_id).service_name
            amount = ServicesList.objects.get(id=service_id).amount
            invoice_obj = InvoiceItem.objects.create(service_item=service_obj, service_name=service_name,
                                                     amount=amount, Payment=payment_obj)
        serializer = PaymentEntrySerializer(payment_obj)
        myJson = {"status": "1", "data": serializer.data}
        return JsonResponse(myJson)


class payment_validate(APIView):
    def post(self,request):
        data = request.data
        id = data['id']
        status= data['status']
        payment_mode = data['mode']
        payment_obj = PaymentEntry.objects.filter(id=id).update(status=status,payment_mode=payment_mode)
        myJson = {"status": "1", "data": "Success"}
        return JsonResponse(myJson)