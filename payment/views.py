from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import uuid
from customer.models import CustomerInfo, VehicleInfo, TestDetails
from users.models import UserType, UserInfo
from .models import PaymentEntry, InvoiceItem
from service.models import ServicesList
from .serializers import PaymentEntrySerializer, InvoiceItemSerializer
from customer.serializers import CustomerInfoSerializer, VehicleInfoSerializer
from .square_api import base_url, client_id, client_secret, grant_type, Content_Type, scope


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

class update_payment_entry(APIView):
    def post(self, request):
        data = request.data
        payment_id = data['id']
        final_amount = data['final_amount']
        tax_offered = data['tax_offered']
        discount_offered = data['discount_offered']
        status = data['status']
        payment_mode = 'Other'
        amount_tendered = 0
        changed_given = 0
        service_item = data['service_item']
        payment_exist = PaymentEntry.objects.get(id=payment_id)
        payment_obj = PaymentEntry.objects.filter(id=payment_id).update(final_amount=final_amount, tax_offered=tax_offered,
                                                  discount_offered=discount_offered, payment_mode=payment_mode,
                                                  status=status, amount_tendered=amount_tendered,
                                                  changed_given=changed_given)
        for i in service_item:
            service_id = i['id']
            service_obj = ServicesList.objects.get(id=service_id)
            service_name = ServicesList.objects.get(id=service_id).service_name
            amount = ServicesList.objects.get(id=service_id).amount
            if InvoiceItem.objects.filter(service_item=service_id,Payment=payment_exist):
                invoice_obj = InvoiceItem.objects.filter(service_item=service_id).update(service_name=service_name,
                                                         amount=amount)
            else:
                invoice_obj = InvoiceItem.objects.create(service_item=service_obj, service_name=service_name,
                                                         amount=amount, Payment=payment_exist)

        updated_list= InvoiceItem.objects.filter(Payment=payment_exist).values_list('service_item', flat=True)
        for i in updated_list:
            dt = 0
            for j in service_item:
                  if j['id'] == i:
                      dt=dt+1
            if dt == 0:
                InvoiceItem.objects.filter(service_item=i).delete()
        payment_exist = PaymentEntry.objects.get(id=payment_id)
        serializer = PaymentEntrySerializer(payment_exist)
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

        myJson = {"status": "1", "data": id}
        return JsonResponse(myJson)


class order_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Vehicle__in=cust2).order_by('-created_date')
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
        total = 0
        count = cust3.count()
        for i in cust3:
            total = total + i.final_amount
        sales = {"sales_count": count, "total_sales": total}
        myJson = {"status": "1", "data": sales}
        return JsonResponse(myJson)

class order_invoice(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        cust2 = PaymentEntry.objects.get(id=session)
        serializer2 = PaymentEntrySerializer(cust2)
        cust3 = InvoiceItem.objects.filter(Payment=cust2)
        serializer = InvoiceItemSerializer(cust3, many=True)
        myJson = {"status": "1", "Invoice": serializer2.data, "Service" : serializer.data}
        return JsonResponse(myJson)



# class create_token(APIView):
#     def post(self, request):
#         data = request.data
#         session = data['id']
#         user_info_obj = UserType.objects.get(id=session)
#         user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
#         # response = requests.get(base_url+'/oauth2/authorize?client_id='+client_id+'&scope='+scope+'&state=82201dd8d83d23cc8a48caf52ba4f4fb')
#         # json_response = response.json()
#         code = 'sq0cgp-7QjQLaly1h999T0dF9LrSA'
#
#         token = requests.post(base_url + '/oauth2/token',
#                               data={"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type,
#                                     "code": code},
#                               headers={"Content-Type": "application/json", "Square-Version": "2021-07-21"})
#         json_response = token.json()
#         square_token = token['access_token"']
#         expires_at = token['expires_at']
#         merchant_id = token['merchant_id']
#         refresh_token = token['refresh_token']
#         SquareTerminal.objects.create(square_token=square_token, expires_at=expires_at, merchant_id=merchant_id,
#                                       refresh_token=refresh_token,
#                                       client=user_obj)
#         myJson = {"status": "1", "data": "success"}
#         return JsonResponse(myJson)
#
#
# class renew_token(APIView):
#     def post(self, request):
#         data = request.data
#         session = data['id']
#         user_info_obj = UserType.objects.get(id=session)
#         user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
#         token = SquareTerminal.objects.get(client=user_obj).square_token
#         new_token = requests.post(base_url + '/oauth2/clients/' + client_id + '/access-token/renew',
#                                   data={"access_token": token, },
#                                   headers={"Authorization": "client  " + client_secret,
#                                            "Content-Type": "application/json", "Square-Version": "2021-07-21"})
#         json_response = new_token.json()
#         square_token = token['access_token"']
#         expires_at = token['expires_at']
#         merchant_id = token['merchant_id']
#         refresh_token = token['refresh_token']
#         SquareTerminal.objects.update(client=user_obj)(square_token=square_token, expires_at=expires_at,
#                                                        merchant_id=merchant_id,
#                                                        refresh_token=refresh_token,
#                                                        client=user_obj)
#         myJson = {"status": "1", "data": "success"}
#         return JsonResponse(myJson)
#
#
# class list_device(APIView):
#     def post(self, request):
#         data = request.data
#         session = data['id']
#         user_info_obj = UserType.objects.get(id=session)
#         user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
#         token = SquareTerminal.objects.get(client=user_obj).square_token
#         list_device = requests.post(base_url + '/v2/devices/codes',
#                                     headers={"Authorization": 'Bearer ' + token,
#                                              "Content-Type": "application/json", "Square-Version": "2021-07-21"})
#         json_response = list_device.json()
#         return JsonResponse(json_response)
#
#
# class get_device(APIView):
#     def post(self, request):
#         data = request.data
#         session = data['id']
#         user_info_obj = UserType.objects.get(id=session)
#         user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
#         token = SquareTerminal.objects.get(client=user_obj).square_token
#         code = SquareDevice.objects.get(client=user_obj).code
#         list_device = requests.post(base_url + '/v2/devices/codes/' + code,
#                                     headers={"Authorization": 'Bearer ' + token,
#                                              "Content-Type": "application/json", "Square-Version": "2021-07-21"})
#         json_response = list_device.json()
#         return JsonResponse(json_response)
#
#
# class create_device(APIView):
#     def post(self, request):
#         data = request.data
#         session = data['id']
#         user_info_obj = UserType.objects.get(id=session)
#         user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
#         token = SquareTerminal.objects.get(client=user_obj).square_token
#         list_device = requests.post(base_url + '/v2/devices/codes/',
#                                     data={"device_code": {"product_type": "TERMINAL_API"}},
#                                     headers={"Authorization": 'Bearer ' + token,
#                                              "Content-Type": "application/json", "Square-Version": "2021-07-21"})
#         json_response = list_device.json()
#         return JsonResponse(json_response)


class create_terminal_checkout(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        amount = data['amount']
        currency = data['currency']
        device_id = data['device_id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        token = SquareTerminal.objects.get(client=user_obj).square_token
        key=uuid.uuid1()
        list_device = requests.post(base_url + '/v2/terminals/checkouts',
                                    data={"idempotency_key": key,
                                          "checkout": {
                                              "amount_money": {
                                                  "amount": amount,
                                                  "currency": currency
                                              },
                                              "device_options": {
                                                  "device_id": device_id
                                              }
                                          }},
                                    headers={"Authorization": 'Bearer ' + token,
                                             "Content-Type": "application/json", "Square-Version": "2021-07-21"})
        json_response = list_device.json()
        return JsonResponse(json_response)
