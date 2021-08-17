from os.path import split

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import uuid
import json
from django.db.models import Q
import datetime
from customer.models import CustomerInfo, VehicleInfo, TestDetails
from users.models import UserType, UserInfo
from .models import PaymentEntry, InvoiceItem,TaxItem,FeesItem,DiscountItem,TestTypeItem,MustHaveItem,SquareDevice,SquareTerminalCheckout
from service.models import ServicesList,Taxes,Discounts,Fees,TestType,MustHave,CashDiscount,SquareCredential
from .serializers import PaymentEntrySerializer, InvoiceItemSerializer,FeesItemSerializer,TaxItemSerializer,\
    DiscountItemSerializer,TestTypeItemSerializer,MustHaveItemSerializer
from customer.serializers import CustomerInfoSerializer, VehicleInfoSerializer
from service.serializers import TestTypeSerializer,MustHaveSerializer,CashDiscountSerializer,SquareCredentialSerializer
from .square_api import base_url


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
class generic_tables(APIView):
    def get(self,request):
        test_type= TestType.objects.all()
        must_have = MustHave.objects.all()
        serializer = TestTypeSerializer(test_type,many=True)
        serializer2 = MustHaveSerializer(must_have,many=True)
        myjson = {"status":"1","tset":serializer.data,"must":serializer2.data}
        return JsonResponse(myjson)

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
        discounts = data['discounts']
        taxes = data['taxes']
        fees = data['fees']
        test_type = data['test_type']
        must_have = data['must_have']
        additional_comments = data['additional_comments']
        veh = VehicleInfo.objects.get(id=vehicle)
        cut = CustomerInfo.objects.get(id=veh.customer_id.id)
        user_obj = UserInfo.objects.get(id=cut.user_id.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        if PaymentEntry.objects.filter(Vehicle__in=cust2).exists():
            count = PaymentEntry.objects.filter(Vehicle__in=cust2).count()
        else:
            count=0
        count = count+1
        if count<= 9 :
            invoice_id = '#Order-0'+ str(count)
        else:
            invoice_id = '#Order-' + str(count)

        payment_obj = PaymentEntry.objects.create(final_amount=final_amount, tax_offered=tax_offered,invoice_id=invoice_id,
                                                      discount_offered=discount_offered, payment_mode=payment_mode,
                                                      status=status, Vehicle=vehicle_obj, amount_tendered=amount_tendered,
                                                      changed_given=changed_given,additional_comments=additional_comments)
        for i in service_item:
                service_id = i['id']
                service_obj = ServicesList.objects.get(id=service_id)
                service_name = ServicesList.objects.get(id=service_id).service_name
                amount = ServicesList.objects.get(id=service_id).amount
                invoice_obj = InvoiceItem.objects.create(service_item=service_obj, service_name=service_name,
                                                         amount=amount, Payment=payment_obj)
        for i in taxes:
                tax_id = i['id']
                tax_obj = Taxes.objects.get(id=tax_id)
                tax_name = Taxes.objects.get(id=tax_id).tax_name
                amount = Taxes.objects.get(id=tax_id).tax_value
                TaxItem.objects.create(tax_item=tax_obj,tax_name=tax_name,amount=amount,Payment=payment_obj)
        for i in fees:
                fees_id = i['id']
                fees_obj = Fees.objects.get(id=fees_id)
                fees_name = Fees.objects.get(id=fees_id).fees_name
                amount = Fees.objects.get(id=fees_id).fees_value
                FeesItem.objects.create(fees_item=fees_obj,fees_name=fees_name,amount=amount,Payment=payment_obj)
        for i in discounts:
                discount_id = i['id']
                discount_obj = Discounts.objects.get(id=discount_id)
                discount_name = Discounts.objects.get(id=discount_id).offer_name
                amount = Discounts.objects.get(id=discount_id).discount_value
                DiscountItem.objects.create(discount_item=discount_obj,offer_name=discount_name,amount=amount,Payment=payment_obj)
        for i in test_type:
                test_id = i['id']
                test_obj = TestType.objects.get(id=test_id)
                test_name = TestType.objects.get(id=test_id).test_type_name
                TestTypeItem.objects.create(test_item=test_obj, test_type_name=test_name,Payment=payment_obj)
        for i in must_have:
                must_id = i['id']
                must_obj = MustHave.objects.get(id=must_id)
                must_name = MustHave.objects.get(id=must_id).must_have_name
                MustHaveItem.objects.create(must_have_item=must_obj, must_have_name=must_name,Payment=payment_obj)
        serializer = PaymentEntrySerializer(payment_obj)
        myJson = {"status": "1", "data": serializer.data}
        return JsonResponse(myJson)


def service_updation(service_item, payment_exist):
    for i in service_item:
        service_id = i['id']
        service_obj = ServicesList.objects.get(id=service_id)
        service_name = ServicesList.objects.get(id=service_id).service_name
        amount = ServicesList.objects.get(id=service_id).amount
        if InvoiceItem.objects.filter(service_item=service_id, Payment=payment_exist):
            invoice_obj = InvoiceItem.objects.filter(service_item=service_id).update(service_name=service_name,
                                                                                     amount=amount)
        else:
            invoice_obj = InvoiceItem.objects.create(service_item=service_obj, service_name=service_name,
                                                     amount=amount, Payment=payment_exist)

    updated_list = InvoiceItem.objects.filter(Payment=payment_exist).values_list('service_item', flat=True)
    for i in updated_list:
        dt = 0
        for j in service_item:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
            InvoiceItem.objects.filter(service_item=i).delete()


def tax_updation(taxes, payment_exist):
    for i in taxes:
        tax_id = i['id']
        tax_obj = Taxes.objects.get(id=tax_id)
        tax_name = Taxes.objects.get(id=tax_id).tax_name
        amount = Taxes.objects.get(id=tax_id).tax_value
        if TaxItem.objects.filter(tax_item=tax_id, Payment=payment_exist):
            TaxItem.objects.filter(tax_item=tax_id).update(tax_name=tax_name,amount=amount)
        else:
            TaxItem.objects.create(tax_item=tax_obj, tax_name=tax_name,amount=amount, Payment=payment_exist)

    updated_list = TaxItem.objects.filter(Payment=payment_exist).values_list('tax_item', flat=True)
    for i in updated_list:
        dt = 0
        for j in taxes:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
            TaxItem.objects.filter(tax_item=i).delete()


def fees_updation(fees, payment_exist):
    for i in fees:
        fees_id = i['id']
        fees_obj = Fees.objects.get(id=fees_id)
        fees_name = Fees.objects.get(id=fees_id).fees_name
        amount = Fees.objects.get(id=fees_id).fees_value
        if FeesItem.objects.filter(fees_item=fees_id, Payment=payment_exist):
            FeesItem.objects.filter(fees_item=fees_id).update(fees_name=fees_name,amount=amount)
        else:
            FeesItem.objects.create(fees_item=fees_obj, fees_name=fees_name,amount=amount, Payment=payment_exist)

    updated_list = FeesItem.objects.filter(Payment=payment_exist).values_list('fees_item', flat=True)
    for i in updated_list:
        dt = 0
        for j in fees:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
            FeesItem.objects.filter(fees_item=i).delete()


def discount_updation(discounts, payment_exist):
    for i in discounts:
        discount_id = i['id']
        discount_obj = Discounts.objects.get(id=discount_id)
        discount_name = Discounts.objects.get(id=discount_id).offer_name
        amount = Discounts.objects.get(id=discount_id).discount_value
        if DiscountItem.objects.filter(discount_item=discount_id, Payment=payment_exist):
            DiscountItem.objects.filter(discount_item=discount_id).update(offer_name=discount_name,amount=amount)
        else:
            DiscountItem.objects.create(discount_item=discount_obj, offer_name=discount_name,amount=amount, Payment=payment_exist)

    updated_list = DiscountItem.objects.filter(Payment=payment_exist).values_list('discount_item', flat=True)
    for i in updated_list:
        dt = 0
        for j in discounts:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
            DiscountItem.objects.filter(discount_item=i).delete()


def test_type_updation(test_type, payment_exist):
    for i in test_type:
        tax_id = i['id']
        tax_obj = TestType.objects.get(id=tax_id)
        if TestTypeItem.objects.filter(test_item=tax_id, Payment=payment_exist):
            pass
        else:
            TestTypeItem.objects.create(test_item=tax_obj,  Payment=payment_exist)

    updated_list = TestTypeItem.objects.filter(Payment=payment_exist).values_list('test_item', flat=True)
    for i in updated_list:
        dt = 0
        for j in test_type:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
            TestTypeItem.objects.filter(test_item=i).delete()


def must_have_updation(must_have, payment_exist):
    for i in must_have:
        tax_id = i['id']
        tax_obj = MustHave.objects.get(id=tax_id)
        if MustHaveItem.objects.filter(must_have_item=tax_id, Payment=payment_exist):
            pass
        else:
            MustHaveItem.objects.create(must_have_item=tax_obj,  Payment=payment_exist)

    updated_list = MustHaveItem.objects.filter(Payment=payment_exist).values_list('must_have_item', flat=True)
    for i in updated_list:
        dt = 0
        for j in must_have:
            if j['id'] == i:
                dt = dt + 1
        if dt == 0:
            MustHaveItem.objects.filter(must_have_item=i).delete()


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
        discounts = data['discounts']
        taxes = data['taxes']
        fees = data['fees']
        test_type = data['test_type']
        must_have = data['must_have']
        additional_comments = data['additional_comments']
        payment_exist = PaymentEntry.objects.get(id=payment_id)
        payment_obj = PaymentEntry.objects.filter(id=payment_id).update(final_amount=final_amount, tax_offered=tax_offered,
                                                  discount_offered=discount_offered, payment_mode=payment_mode,
                                                  status=status, amount_tendered=amount_tendered,
                                                  changed_given=changed_given,additional_comments=additional_comments)
        none_response=service_updation(service_item,payment_exist)
        none_response =tax_updation(taxes,payment_exist)
        none_response = fees_updation(fees, payment_exist)
        none_response = discount_updation(discounts, payment_exist)
        none_response = test_type_updation(test_type, payment_exist)
        none_response = must_have_updation(must_have, payment_exist)
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
        cust3 = PaymentEntry.objects.filter(Vehicle__in=cust2).order_by('-invoice_id')
        if SquareCredential.objects.filter(client=user_obj).exists():
            token = SquareCredential.objects.get(client=user_obj).accees_token
            checkout_id = SquareTerminalCheckout.objects.filter(payment__in=cust3)
            for i in checkout_id:
                checkout = requests.get(base_url + '/v2/terminals/checkouts/' + i.checkout_id,
                                        headers={"Authorization": 'Bearer ' + token,
                                                 "Content-Type": "application/json", "Square-Version": "2021-07-21"})
                json_response = checkout.json()
                status = json_response['checkout']['status']
                PaymentEntry.objects.filter(id=i.payment.id).update(status=status)
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
        veh = VehicleInfo.objects.get(id=cust2.Vehicle.id)
        cut = CustomerInfo.objects.get(id=veh.customer_id.id)
        user_obj = UserInfo.objects.get(id=cut.user_id.id)
        serializer2 = PaymentEntrySerializer(cust2)
        cust3 = InvoiceItem.objects.filter(Payment=cust2)
        serializer = InvoiceItemSerializer(cust3, many=True)
        cust4 = FeesItem.objects.filter(Payment=cust2)
        serializer3 = FeesItemSerializer(cust4, many=True)
        cust5 = TaxItem.objects.filter(Payment=cust2)
        serializer4 = TaxItemSerializer(cust5, many=True)
        cust6 = DiscountItem.objects.filter(Payment=cust2)
        serializer5 = DiscountItemSerializer(cust6, many=True)
        cust7 = TestTypeItem.objects.filter(Payment=cust2)
        serializer6 = TestTypeItemSerializer(cust7, many=True)
        cust8 = MustHaveItem.objects.filter(Payment=cust2)
        serializer7 = MustHaveItemSerializer(cust8, many=True)
        cust9 = CashDiscount.objects.get(client=user_obj)
        serializer8 = CashDiscountSerializer(cust9)
        myJson = {"status": "1", "Invoice": serializer2.data, "Service" : serializer.data, "Fees":serializer3.data,
                  "Taxes": serializer4.data, "Discounts" : serializer5.data,"test_type": serializer6.data,
                  "must":serializer7.data, "Cash_discount" : serializer8.data}
        return JsonResponse(myJson)


class confirm_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Q(status ='Completed') | Q(status='COMPLETED'),Vehicle__in=cust2).order_by('-invoice_id')
        serializer = PaymentEntrySerializer(cust3, many=True)
        myJson = {"status": "1", "data": serializer.data}
        return JsonResponse(myJson)

class datewise_order_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        first = data['first_date']
        last = data['last_date']
        year,month,date =first.split('-')
        year=int(year)
        month=int(month)
        date=int(date)
        last_year, last_month, last_date = last.split('-')
        last_year = int(last_year)
        last_month = int(last_month)
        last_date = int(last_date)
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Q(status ='Completed') | Q(status='COMPLETED'),created_date__date__range=(datetime.date(year,month,date), datetime.date(last_year,last_month,last_date)), Vehicle__in=cust2).order_by('-invoice_id')
        serializer = PaymentEntrySerializer(cust3, many=True)
        myJson = {"status": "1", "data":serializer.data}
        return JsonResponse(myJson)

class datewise_customer_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        first = data['first_date']
        last = data['last_date']
        year,month,date =first.split('-')
        year=int(year)
        month=int(month)
        date=int(date)
        last_year, last_month, last_date = last.split('-')
        last_year = int(last_year)
        last_month = int(last_month)
        last_date = int(last_date)
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust3 = VehicleInfo.objects.filter(customer_id__in=customer_obj,created_date__date__range=(datetime.date(year,month,date), datetime.date(last_year,last_month,last_date)))
        serializer = VehicleInfoSerializer(cust3, many=True)
        myJson = {"status": "1", "data":serializer.data}
        return JsonResponse(myJson)

class delete_customer(APIView):
    def post(self,request):
        data = request.data
        session = data['vehicle_id']
        vehicle_obj=VehicleInfo.objects.get(id=session)
        if PaymentEntry.objects.filter(Vehicle=vehicle_obj).exists():
            myJson = {"status": "0", "data": "Order_Exist"}
            return JsonResponse(myJson)
        else:
            VehicleInfo.objects.filter(id=session).delete()
            myJson = {"status": "1", "data": "Deleted"}
            return JsonResponse(myJson)

#
# class create_token(APIView):
#     def post(self, request):
#         data = request.data
#         session = data['id']

        # user_info_obj = UserType.objects.get(id=session)
        # user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        # code = requests.get(base_url+'/oauth2/authorize?client_id='+client_id+'$scope='+scope+'$state=82201dd8d83d23cc8a48caf52ba4f4fb')
        # code = requests.get('https://connect.squareup.com/oauth2/authorize?client_id=sq0idp-VG89cPXiW7WgdpQIAZNR3A&scope=CUSTOMERS_WRITE+CUSTOMERS_READ+PAYMENTS_WRITE_IN_PERSON+MERCHANT_PROFILE_READ+PAYMENTS_READ+PAYMENTS_WRITE+PAYMENTS_WRITE_ADDITIONAL_RECIPIENTS+ORDERS_READ+ORDERS_WRITE+DEVICE_CREDENTIAL_MANAGEMENT&state=82201dd8d83d23cc8a48caf52ba4f4fb')
        # print(code)
        # code = 'sq0cgp-7QjQLaly1h999T0dF9LrSA'
        #
        # token = requests.post(base_url + '/oauth2/token',
        #                       data={"client_id": client_id, "client_secret": client_secret, "grant_type": "authorization_code",
        #                             "code": code},
        #                       headers={"Content-Type": "application/json", "Square-Version": "2021-07-21"})
        # json_response = token.json()
        # square_token = token['access_token"']
        # expires_at = token['expires_at']
        # token_type = token['token_type']
        # merchant_id = token['merchant_id']
        # refresh_token = token['refresh_token']
        # sq_token=SquareTerminal.objects.create(square_token=square_token, expires_at=expires_at, merchant_id=merchant_id,
        #                               refresh_token=refresh_token,
        #                               client=user_obj)
        # serializer =
        # myJson = {"status": "1", "data": "success"}
        # return JsonResponse(myJson)

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
#         token = SquareCredential.objects.get(client=user_obj).accees_token
#         location_id = SquareCredential.objects.get(client=user_obj).location_id
#         list_device = requests.get(base_url + '/v2/devices/codes?product_type=TERMINAL_API&location_id='+ location_id,
#                                     headers={"Authorization": 'Bearer ' + token,
#                                              "Content-Type": "application/json", "Square-Version": "2021-07-21"})
#         json_response = list_device.json()
#         myJson = {"status": "1", "data": json_response}
#         return JsonResponse(myJson)

class get_device(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if SquareDevice.objects.filter(client=user_obj).exists():
            token = SquareCredential.objects.get(client=user_obj).accees_token
            code = SquareDevice.objects.get(client=user_obj).square_id
            list_device = requests.get(base_url + '/v2/devices/codes/' + code,
                                        headers={"Authorization": 'Bearer ' + token,
                                                 "Content-Type": "application/json", "Square-Version": "2021-07-21"})
            json_response = list_device.json()
            status=json_response['device_code']['status']
            if status=="PAIRED":
                device_id = json_response['device_code']['device_id']
                SquareDevice.objects.filter(square_id=code).update(status=status,device_id=device_id)
            myJson = {"status": "1", "data": json_response}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)


class create_device(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        token = SquareCredential.objects.get(client=user_obj).accees_token
        location_id = SquareCredential.objects.get(client=user_obj).location_id
        key = uuid.uuid1()
        vaule = {"device_code": {"product_type": "TERMINAL_API"}, "idempotency_key": str(key)}
        list_device = requests.post(base_url + '/v2/devices/codes/',
                                    data=json.dumps(vaule),
                                    headers={"Authorization": 'Bearer ' + token,
                                             "Content-Type": "application/json", "Square-Version": "2021-07-21"})
        json_response = list_device.json()
        device_id=json_response["device_code"]["id"]
        name = json_response["device_code"]["name"]
        code = json_response["device_code"]["code"]
        location_id= json_response["device_code"]["location_id"]
        status = json_response["device_code"]["status"]
        SquareDevice.objects.create(square_id=device_id,name=name,code=code,location=location_id,status=status,
                                            client=user_obj)
        myJson = {"status": "1", "data": json_response}
        return JsonResponse(myJson)


class create_terminal_checkout(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        payment_id = data['payment_id']
        amount = data['amount']
        currency = data['currency']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if SquareDevice.objects.filter(client=user_obj,status="PAIRED").exists():
            token = SquareCredential.objects.get(client=user_obj).accees_token
            device_id = SquareDevice.objects.get(client=user_obj).device_id
            key=uuid.uuid1()
            value={"idempotency_key": str(key),
                    "checkout": {
                                "amount_money": { "amount": amount,
                                                  "currency": currency
                                                  },
                                                  "device_options": {
                                                      "device_id": device_id
                                                  }
                                }}
            list_device = requests.post(base_url + '/v2/terminals/checkouts',
                                        data=json.dumps(value),
                                        headers={"Authorization": 'Bearer ' + token,
                                                 "Content-Type": "application/json", "Square-Version": "2021-07-21"})
            json_response = list_device.json()
            checkout_id = json_response['checkout']['id']
            checkout_status = json_response['checkout']['status']
            payment= PaymentEntry.objects.get(id=payment_id)
            SquareTerminalCheckout.objects.create(checkout_id=checkout_id,client=user_obj,payment=payment)
            PaymentEntry.objects.filter(id=payment_id).update(status=checkout_status,payment_mode="Card")
            myJson = {"status": "1", "data": json_response}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": "error"}
            return JsonResponse(myJson)

