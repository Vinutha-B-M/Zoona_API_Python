from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from customer.models import CustomerInfo, VehicleInfo, TestDetails
from users.models import UserType, UserInfo
from .models import PaymentEntry, InvoiceItem
from service.models import ServicesList
from .serializers import PaymentEntrySerializer, InvoiceItemSerializer
from customer.serializers import CustomerInfoSerializer, VehicleInfoSerializer


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
        payment_mode = 'Other'
        amount_tendered = 0
        changed_given = 0
        vehicle_obj = VehicleInfo.objects.get(id=vehicle)
        service_item = data['service_item']
        payment_obj = PaymentEntry.objects.create(final_amount=final_amount, tax_offered=tax_offered,
                                                  discount_offered=discount_offered, payment_mode=payment_mode,
                                                  status=status, Vehicle=vehicle_obj, amount_tendered=amount_tendered,
                                                  changed_given=changed_given)
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
    def post(self, request):
        data = request.data
        id = data['id']
        status = data['status']
        payment_mode = data['mode']
        amount_tendered = data['amount_tendered']
        changed_given = data['changed_given']
        payment_obj = PaymentEntry.objects.filter(id=id).update(status=status, payment_mode=payment_mode,
                                                                changed_given=changed_given,
                                                                amount_tendered=amount_tendered)
        myJson = {"status": "1", "data": "Success"}
        return JsonResponse(myJson)


class order_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Vehicle__in=cust2)
        serializer = PaymentEntrySerializer(cust3, many=True)
        myJson = {"status": "1", "data": serializer.data}
        return JsonResponse(myJson)


class total_sales(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Vehicle__in=cust2)
        total=0
        count = cust3.count()
        for i in cust3:
            total=total+i.final_amount
        sales = {"sales_count": count, "total_sales": total}
        myJson = {"status": "1", "data": sales }
        return JsonResponse(myJson)
