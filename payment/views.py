from os.path import split

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import uuid
import json
from django.db.models.functions import (
  ExtractDay, ExtractMonth, ExtractQuarter, ExtractWeek,
  ExtractWeekDay, ExtractYear,
)
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
import datetime
from customer.models import CustomerInfo, VehicleInfo, TestDetails
from users.models import UserType, UserInfo
from .models import PaymentEntry, InvoiceItem,TaxItem,FeesItem,DiscountItem,TestTypeItem,MustHaveItem,SquareDevice,\
    SquareTerminalCheckout,FortisPayCredentials
from service.models import ServicesList,Taxes,Discounts,Fees,TestType,MustHave,CashDiscount,SquareCredential
from .serializers import PaymentEntrySerializer, InvoiceItemSerializer,FeesItemSerializer,TaxItemSerializer,\
    DiscountItemSerializer,TestTypeItemSerializer,MustHaveItemSerializer,FortisPaySerializer
from customer.serializers import CustomerInfoSerializer, VehicleInfoSerializer
from service.serializers import TestTypeSerializer,MustHaveSerializer,CashDiscountSerializer,SquareCredentialSerializer
from .square_api import base_url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# ..............................invoice_generic_entry..............................
class generic_tables(APIView):
    def get(self,request):
        test_type= TestType.objects.all()
        must_have = MustHave.objects.all()
        serializer = TestTypeSerializer(test_type,many=True)
        serializer2 = MustHaveSerializer(must_have,many=True)
        myjson = {"status":"1","tset":serializer.data,"must":serializer2.data}
        return JsonResponse(myjson)


# ...............................Invoice-Entry-Into-Table...............................


class payment_entry(APIView):
    def post(self, request):
        data = request.data
        final_amount = data['final_amount']
        card_amount = data['card_amount']
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
        now = datetime.datetime.now()
        year=now.year%100
        if count<= 9 :
            if now.day <= 9:
                if now.month <= 9:
                    invoice_id = '0' + str(now.month) +'0' +str(now.day) + str(year) + '00' + str(count)
                else:
                    invoice_id =str(now.month) +'0'+ str(now.day) + str(year) + '00' + str(count)
            else:
                if now.month <= 9:
                    invoice_id = '0' + str(now.month)  + str(now.day) + str(year) + '00' + str(count)
                else:
                    invoice_id = str(now.month) +  str(now.day) + str(year) + '00' + str(count)
        elif count<= 99:
            if now.day <= 9:
                if now.month <= 9:
                    invoice_id = '0' + str(now.month) + '0' + str(now.day) + str(year) + '0' + str(count)
                else:
                    invoice_id = str(now.month) + '0' + str(now.day) + str(year) + '0' + str(count)
            else:
                if now.month <= 9:
                    invoice_id = '0' + str(now.month) + str(now.day) + str(year) + '0' + str(count)
                else:
                    invoice_id = str(now.month) + str(now.day) + str(year) + '0' + str(count)
        else:
            if now.day <= 9:
                if now.month <= 9:
                    invoice_id = '0' + str(now.month) + '0' + str(now.day) + str(year)  + str(count)
                else:
                    invoice_id = str(now.month) + '0' + str(now.day) + str(year)  + str(count)
            else:
                if now.month <= 9:
                    invoice_id = '0' + str(now.month) + str(now.day) + str(year)  + str(count)
                else:
                    invoice_id = str(now.month) + str(now.day) + str(year)  + str(count)

        payment_obj = PaymentEntry.objects.create(final_amount=final_amount, tax_offered=tax_offered,invoice_id=invoice_id,
                                                  discount_offered=discount_offered, payment_mode=payment_mode,status=status,
                                                  Vehicle=vehicle_obj, amount_tendered=amount_tendered,card_amount=card_amount,
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

# ...............................END-Invoice-Entry-Into-Table...............................

# ...............................Services-Update-Function-Of-Invoice...............................

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
            InvoiceItem.objects.filter(service_item=i,Payment=payment_exist).delete()

# ...............................END-Services-Update-Function-Of-Invoice...............................

# ...............................Taxes-Update-Function-Of-Invoice......................................

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
            TaxItem.objects.filter(tax_item=i,Payment=payment_exist).delete()

# ...............................END-Taxes-Update-Function-Of-Invoice......................................

# ...............................Fees-Update-Function-Of-Invoice......................................

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
            FeesItem.objects.filter(fees_item=i,Payment=payment_exist).delete()

# ...............................END-Fees-Update-Function-Of-Invoice......................................

# ...............................Discounts-Update-Function-Of-Invoice......................................

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

# ...............................END-Discounts-Update-Function-Of-Invoice......................................

# ...............................TestType-Update-Function-Of-Invoice......................................

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
            TestTypeItem.objects.filter(test_item=i,Payment=payment_exist).delete()

# ...............................END-TestType-Update-Function-Of-Invoice......................................

# ...............................MustHave-Update-Function-Of-Invoice......................................

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
            MustHaveItem.objects.filter(must_have_item=i,Payment=payment_exist).delete()

# ...............................END-MustHave-Update-Function-Of-Invoice......................................

# ...............................Invoice-Update-......................................

class update_payment_entry(APIView):
    def post(self, request):
        data = request.data
        payment_id = data['id']
        final_amount = data['final_amount']
        card_amount = data['card_amount']
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
                                                  status=status, amount_tendered=amount_tendered,card_amount=card_amount,
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
# ...............................END-Invoice-Update-......................................

# ...............................Invoice-Validate-After-Payment......................................

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

# ...............................END-Invoice-Validate-After-Payment......................................

# ...............................Invoice-List......................................
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

# ...............................END-Invoice-List......................................

# ...............................Invoice-List-Pagination-Number......................................
class order_list_page(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        page_no = data['page_number']
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
        items_per_page = 5
        total_count = cust3.count()
        pages = 0
        if total_count > 0:
            pages = total_count / items_per_page
            if pages % 1 == 0:
                pass
            else:
                pages = int(pages)
                pages = pages + 1
        paginator = Paginator(cust3, items_per_page)
        page_num = page_no
        pages_data = {}
        if pages < page_num:
            pages_data['current_page'] = pages
        else:
            pages_data['current_page'] = page_num
        pages_data['total_pages'] = pages
        try:
            cust3 = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            cust3 = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            cust3 = paginator.page(paginator.num_pages)
        serializer = PaymentEntrySerializer(cust3, many=True)
        info={}
        info['current_page']=page_num
        info['total_pages']=pages
        myJson = {"status": "1", "data": serializer.data,"page_info":info}
        return JsonResponse(myJson)

# ...............................END-Invoice-List-Pagination-Number......................................

# ...............................Invoice-List-Count-With-Completed-Or-Without Completed..................
class total_sales(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Q(status ='Completed') | Q(status='COMPLETED'),Vehicle__in=cust2)
        cust4 = PaymentEntry.objects.filter(Q(status ='Completed') | Q(status='COMPLETED'),Vehicle__in=cust2).count()

        total = 0
        count = cust3.count()
        for j in cust3:
            if j.payment_mode == 'cash':
                total =round( total + j.final_amount,2)
            else:
                total =round( total + j.card_amount,2)
        sales = {"sales_count": cust4, "total_sales": total}
        myJson = {"status": "1", "data": sales}
        return JsonResponse(myJson)
# ...............................END-Invoice-List-Count-With-Completed-Or-Without Completed..................

# ...............................Single-Invoice......................................
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
        if CashDiscount.objects.filter(client=user_obj).exists():
            cust9 = CashDiscount.objects.get(client=user_obj)
            serializer8 = CashDiscountSerializer(cust9)
            myJson = {"status": "1", "Invoice": serializer2.data, "Service" : serializer.data, "Fees":serializer3.data,
                  "Taxes": serializer4.data, "Discounts" : serializer5.data,"test_type": serializer6.data,
                  "must":serializer7.data, "Cash_discount" : serializer8.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "Invoice": serializer2.data, "Service": serializer.data, "Fees": serializer3.data,
                      "Taxes": serializer4.data, "Discounts": serializer5.data, "test_type": serializer6.data,
                      "must": serializer7.data, "Cash_discount": ""}
            return JsonResponse(myJson)

# ...............................END-Single-Invoice......................................

# ...............................Only-Confirm-Invoice-List......................................

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

# ...............................End-Only-Confirm-Invoice-List......................................

# ...............................Date-Wise-Invoice-List......................................

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

# ...............................END-Date-Wise-Invoice-List......................................

# ...............................Date-Wise-Customer-List......................................

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

# ...............................Date-Wise-Customer-List......................................

# ...............................Delete-Customer..............................................

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

# ...............................END-Delete-Customer..............................................

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

# ...............................Square-Device-Info..............................................

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

            device = SquareDevice.objects.get(client=user_obj).id
            status=json_response['device_code']['status']
            if status=="PAIRED":
                device_id = json_response['device_code']['device_id']
                SquareDevice.objects.filter(square_id=code).update(status=status,device_id=device_id)
            if status=="EXPIRED":
                SquareDevice.objects.filter(square_id=code).update(status=status)

            myJson = {"status": "1", "data": json_response,"device":device}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)

# ...............................END-Square-Device-Info..............................................

# ...............................Square-Device-Delete..............................................
class delete_device(APIView):
    def post(self,request):
        data = request.data
        session = data['id']
        if SquareDevice.objects.filter(id=session).exists():
            SquareDevice.objects.filter(id=session).delete()
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)

# ...............................END-Square-Device-Delete..............................................

# ...............................Create-Square-Device..............................................
class create_device(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if SquareDevice.objects.filter(client=user_obj).exists():
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)
        else:
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

# ...............................END-Create-Square-Device..............................................
# ...............................Re-Create-Square-Device..............................................

class recreate_device(APIView):
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
        SquareDevice.objects.filter(client=user_obj).update(square_id=device_id,name=name,code=code,location=location_id,status=status,
                                            client=user_obj)
        myJson = {"status": "1", "data": json_response}
        return JsonResponse(myJson)

# ...............................END-Re-Create-Square-Device..............................................
# ...............................-Square-Terminal-Checkout..............................................

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

# ...............................END-Square-Terminal-Checkout..............................................
# .............................. Fortispay-Credentials-Insert............................


class fortispay_credentials(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        username = data['username']
        password = data['password']
        domain = data['domain']
        response = requests.post('https://api.sandbox.zeamster.com/v2/token',
                                 json={"username": username, "password": password,
                                       "domain": domain}, headers={"developer-id": "jKAdBXmQ"})
        json_response = response.json()
        if 'message' in json_response:
            if json_response['message'] == 'invalid user':
                myJson = {"status": "0", "data": "invalid user"}
                return JsonResponse(myJson)
            if json_response['message'] == 'invalid password':
                myJson = {"status": "0", "data": "invalid password"}
                return JsonResponse(myJson)
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if FortisPayCredentials.objects.filter(username=username,domain=domain,client=user_obj).exists():
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            FortisPayCredentials.objects.create(username=username,password=password,domain=domain,client=user_obj)
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)

# ..............................END-Fortispay-Credentials-Insert............................
# ..............................Update-Fortispay-Credentials............................

class fortispay_update_credentials(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        username = data['username']
        password = data['password']
        domain = data['domain']
        response = requests.post('https://api.sandbox.zeamster.com/v2/token',
                                 json={"username": username, "password": password,
                                       "domain": domain}, headers={"developer-id": "jKAdBXmQ"})
        json_response = response.json()
        if 'message' in json_response:
            if json_response['message'] == 'invalid user':
                myJson = {"status": "0", "data": "invalid user"}
                return JsonResponse(myJson)
            if json_response['message'] == 'invalid password':
                myJson = {"status": "0", "data": "invalid password"}
                return JsonResponse(myJson)
        if FortisPayCredentials.objects.filter(id=session).exists():
            FortisPayCredentials.objects.filter(id=session).update(username=username, password=password, domain=domain)
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": "error"}
            return JsonResponse(myJson)
# ..............................END-Update-Fortispay-Credentials............................
# ..............................Get-Fortispay-Credentials............................

class fortispay(APIView):
    def post(self,request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if FortisPayCredentials.objects.filter(client=user_obj).exists():
            view=FortisPayCredentials.objects.get(client=user_obj)
            serializer=FortisPaySerializer(view)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)

# ..............................END-Get-Fortispay-Credentials............................
# ..............................TErminal-List-Fortispay............................

class fortispay_terminal_list(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if FortisPayCredentials.objects.get(client=user_obj).exists():
            username=FortisPayCredentials.objects.get(client=user_obj).username
            password = FortisPayCredentials.objects.get(client=user_obj).password
            domain = FortisPayCredentials.objects.get(client=user_obj).domain
            response = requests.post('https://api.sandbox.zeamster.com/v2/token',
                                     json={"username": username, "password": password,
                                           "domain": domain}, headers={"developer-id": "jKAdBXmQ"})
            json_response = response.json()
            token_id = json_response['token']['token']
            response = requests.get('https://api.sandbox.zeamster.com/v2/terminals?access-token=' + token_id,
                                    headers={"developer-id": "jKAdBXmQ"}
                                    )
            json_response = response.json()
            return JsonResponse(json_response)
        else:
            myJson = {"status": "0", "data": "FortisPay Account Is Not Linked"}
            return JsonResponse(myJson)

# ..............................END-Terminal-List-Fortispay............................

# @csrf_exempt
# def view_single_transaction(request, transaction_id):
#     response = requests.post('https://api.sandbox.zeamster.com/v2/token',
#                              json={"username": "vikas@zunaco.com", "password": "Goalsr@123",
#                                    "domain": "zunacoqvtizw.sandbox.zeamster.com"}, headers={"developer-id": "jKAdBXmQ"})
#
#     json_response = response.json()
#     token_id = json_response['token']['token']
#
#     response = requests.get(
#         'https://api.sandbox.zeamster.com/v2/transactions/' + transaction_id + '?access-token=' + token_id,
#         headers={"developer-id": "jKAdBXmQ"}
#         )
#     json_response = response.json()
#
#     return JsonResponse(json_response)
#
# ..............................Terminal-Transaction-Fortispay............................

class get_router_transaction(APIView):
        def post(self, request):
            data = request.data
            session = data['id']
            order_id = data['order_id']
            terminal_id = data['terminal_id']
            location_id = data['location_id']
            user_info_obj = UserType.objects.get(id=session)
            user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
            username = FortisPayCredentials.objects.get(client=user_obj).username
            password = FortisPayCredentials.objects.get(client=user_obj).password
            domain = FortisPayCredentials.objects.get(client=user_obj).domain
            response = requests.post('https://api.sandbox.zeamster.com/v2/token',
                                     json={"username": username, "password": password,
                                           "domain": domain}, headers={"developer-id": "jKAdBXmQ"})
            json_response = response.json()
            token_id = json_response['token']['token']
            if PaymentEntry.objects.filter(id=order_id).exists() :
                amount=PaymentEntry.objects.get(id=order_id).card_amount
                amount=float(amount)
            data = {
                "routertransaction":{
                    "payment_method": "cc",
                    "action": "sale",
                    "location_id": location_id,
                    "transaction_amount": amount,
                    "terminal_id": terminal_id,
                    "billing_zip": ""
                }
            }
            response = requests.post('https://api.sandbox.zeamster.com/v2/routertransactions?access-token=' + token_id,
                                     headers={"developer-id": "jKAdBXmQ"},
                                    json=data,
                                    )
            json_response = response.json()
            return JsonResponse(json_response)

# ..............................End-Terminal-Transaction-Fortispay............................
# .............................. Stats............................
def year_month_day_find(cust2):
    now = datetime.datetime.now()
    year = None
    month = None
    day = None
    cust4 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'), Vehicle__in=cust2).last()
    cust5 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'), Vehicle__in=cust2).first()
    year=cust5.created_date.strftime("%Y")
    month=cust5.created_date.strftime("%m")
    day=cust5.created_date.strftime("%d")
    year = int(year)
    month = int(month)
    day = int(day)
    last_year = None
    last_month = None
    last_day = None
    last_year= cust4.created_date.strftime("%Y")
    last_month= cust4.created_date.strftime("%m")
    last_day= cust4.created_date.strftime("%d")
    last_year = int(last_year)
    last_month = int(last_month)
    last_day = int(last_day)
    return year,month,day,last_year,last_month,last_day


def yearwisedata(cust2):
    year_wise_stats = []

    cust3 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),
                                                Vehicle__in=cust2)
    total = 0.0
    total2 = 0.0
    tax = 0.0
    discount = 0.0
    if cust3.count() != 0:
        stats = {}
        for j in cust3:
            if j.payment_mode=='cash':
                total = total + j.final_amount
                total2 = total2+ j.final_amount
                tax = tax + j.tax_offered
                discount = discount+ j.discount_offered
            else:
                total = total + j.card_amount
                tax = tax + j.tax_offered
                discount = discount + j.discount_offered

        stats['gross_amount'] = round( total,2)
        stats['cash_amount'] = round( total2,2)
        stats['card_amount'] = round( total-total2,2)
        stats['taxes']= round(tax,2)
        stats['cash_discount']=round(discount,2)
        year_wise_stats.append(stats)

    return year_wise_stats


def yearwiseservices(cust2, user_obj):
    service_wise_stats = []
    cust3 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),Vehicle__in=cust2)
    invoice = InvoiceItem.objects.filter(Payment__in=cust3)
    if invoice.count() != 0:
        service = ServicesList.objects.filter(client=user_obj)
        for k in service:
            count = 0
            services = {}
            for l in invoice:
                if l.service_item.id == k.id:
                    count = count + 1
            services['service_name'] = k.service_name
            services['count'] = count
            per = round( count*100/cust3.count(),2)
            services['percentage'] = str(per) + '%'
            service_wise_stats.append(services)
    return service_wise_stats


def monthwisedata(month_list, cust2):
    month_wise_stats = []
    for i in month_list:
            cust3 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),
                                                Vehicle__in=cust2, created_date__month__gte=i, created_date__month__lte=i)
            total = 0.0
            total2 = 0.0
            tax = 0.0
            discount = 0.0
            if cust3.count() != 0:
                stats = {}
                for j in cust3:
                    if j.payment_mode == 'cash':
                        total = total + j.final_amount
                        total2 = total2 + j.final_amount
                        tax = tax + j.tax_offered
                        discount = discount + j.discount_offered
                    else:
                        total = total + j.card_amount
                        tax = tax + j.tax_offered
                        discount = discount + j.discount_offered
                stats['year'] = '2021'
                stats['month'] = i
                stats['Gross_Sales'] = round( total,2)
                stats['Cash_Amount'] = round( total2,2)
                stats['Card_Amount'] = round( total - total2,2)
                stats['Tax_Amount'] = round( tax,2)
                stats['Discount_Amount'] = round( discount,2)
                month_wise_stats.append(stats)
    return month_wise_stats

def daywisedata(month_list, cust2,day_list):
    Day_wise_stats = []
    for i in month_list:
        for k in day_list:
            cust3 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),
                                                Vehicle__in=cust2, created_date__month__gte=i,
                                                created_date__month__lte=i,created_date__day__lte=k,
                                                created_date__day__gte=k)
            total = 0.0
            cash = 0.0
            tax = 0.0
            discount = 0.0
            if cust3.count() != 0:
                stats = {}
                for j in cust3:
                    if j.payment_mode == 'cash':
                        total = round( total + j.final_amount,2)
                        cash = round( cash + j.final_amount,2)
                        tax = round( tax + j.tax_offered,2)
                        discount = round(discount + j.discount_offered,2)
                    else:
                        total =round( total + j.card_amount,2)
                        tax =round( tax + j.tax_offered,2)
                        discount =round (discount + j.discount_offered,2)

                stats['Date']= str(k)+'-'+str(i)+'-'+'2021'
                stats['Gross_Sales'] = round( total,2)
                stats['Cash_Amount'] = round( cash,2)
                stats['Card_Amount'] = round( total - cash,2)
                stats['Tax_Amount'] = round( tax,2)
                stats['Discount_Amount'] = round( discount,2)
                Day_wise_stats.append(stats)
    return Day_wise_stats

def weeklydata(cust2):
    card_data=PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),Q(payment_mode='Card') | Q(payment_mode='card'), Vehicle__in=cust2)\
        .annotate(week=ExtractWeek('created_date')).values('week').annotate(card_total=Sum('card_amount')).annotate(tax_offered=Sum('tax_offered')).annotate(discount_offered=Sum('discount_offered')).order_by('week')
    cash_data = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'), Vehicle__in=cust2,payment_mode='cash' )\
        .annotate(week=ExtractWeek('created_date')).values('week').annotate(cash_total=Sum('final_amount')).annotate(tax_offered=Sum('tax_offered')).annotate(discount_offered=Sum('discount_offered')).order_by('week')

    week_data=[]
    if cash_data.count()!=0:
        for i in cash_data:
            if card_data.count() != 0:
                for j in card_data:
                    if i['week']==j['week']:
                        data={}
                        data['week']=i['week']
                        data['Gross_Sales']=round( i['cash_total']+j['card_total'],2)
                        data['card_amount']=round( j['card_total'],2)
                        data['cash_amount']=round( i['cash_total'],2)
                        data['tax_amount']=round( i['tax_offered']+j['tax_offered'],2)
                        data['discount_amount']=round( i['discount_offered']+j['discount_offered'],2)
                        week_data.append(data)
    week=[]
    for i in week_data:
        week.append(i['week'])
    for j in cash_data:
        if j['week'] not in week:
            data = {}
            data['week'] = j['week']
            data['Gross_Sales'] =round( j['cash_total'],2)
            data['card_amount'] = ''
            data['cash_amount'] =  round( j['cash_total'],2)
            data['tax_amount'] = round( j['tax_offered'],2)
            data['discount_amount'] =round( j['discount_offered'],2)
            week_data.append(data)
    week = []
    for i in week_data:
        week.append(i['week'])
    for j in card_data:
        if j['week'] not in week:
            data = {}
            data['week'] = j['week']
            data['Gross_Sales'] =round( j['card_total'],2)
            data['card_amount'] =round( j['card_total'],2)
            data['cash_amount'] = ''
            data['tax_amount'] =round( j['tax_offered'],2)
            data['discount_amount'] =round( j['discount_offered'],2)
            week_data.append(data)
    week_data.sort(key=lambda x: x["week"])
    return week_data

class stats_daily(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        month_list = [1,2,3,4,5,6,7,8,9,10,11,12]
        day_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        day_wise_data = daywisedata(month_list, cust2, day_list)
        myJson = {"status": "1", "Day_Data":day_wise_data}
        return JsonResponse(myJson, safe=False)

class stats_monthly(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        month_list = [1,2,3,4,5,6,7,8,9,10,11,12]
        month_wise_data = monthwisedata(month_list,cust2)
        myJson = {"status": "1", "monthly_Data":month_wise_data}
        return JsonResponse(myJson, safe=False)

class stats_weekly(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        weekly_data = weeklydata(cust2)
        myJson = {"status": "1", "Weekly_Data":weekly_data}
        return JsonResponse(myJson, safe=False)

class stats_services(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        year_wise_data = yearwisedata(cust2)
        year_wise_servies = yearwiseservices(cust2,user_obj)
        myJson = {"status": "1", "Services":year_wise_servies}
        return JsonResponse(myJson, safe=False)

class stats_overall(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        year_wise_data = yearwisedata(cust2)
        myJson = {"status": "1", "stats_overall":year_wise_data}
        return JsonResponse(myJson, safe=False)

def filterwisedata(cust3):
        month_wise_stats = []
        total = 0.0
        total2 = 0.0
        tax = 0.0
        discount = 0.0
        if cust3.count() != 0:
            stats = {}
            for j in cust3:
                if j.payment_mode == 'cash':
                    total = total + j.final_amount
                    total2 = total2 + j.final_amount
                    tax = tax + j.tax_offered
                    discount = discount + j.discount_offered
                else:
                    total = total + j.card_amount
                    tax = tax + j.tax_offered
                    discount = discount + j.discount_offered

            stats['Gross_Sales'] = round( total,2)
            stats['Cash_Amount'] = round( total2,2)
            stats['Card_Amount'] = round( total - total2,2)
            stats['Tax_Amount'] = round( tax,2)
            stats['Discount_Amount'] = round( discount,2)
            month_wise_stats.append(stats)
        return month_wise_stats


class stats_filter(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        first = data['first_date']
        last = data['last_date']
        year, month, date = first.split('-')
        year = int(year)
        month = int(month)
        date = int(date)
        last_year, last_month, last_date = last.split('-')
        last_year = int(last_year)
        last_month = int(last_month)
        last_date = int(last_date)
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),created_date__date__range=(datetime.date(year,month,date), datetime.date(last_year,last_month,last_date)),
                                            Vehicle__in=cust2)
        year_wise_data = filterwisedata(cust3)
        myJson = {"status": "1", "filter_stats":year_wise_data}
        return JsonResponse(myJson, safe=False)


def filterservices(cust3, user_obj):
    service_wise_stats = []
    invoice = InvoiceItem.objects.filter(Payment__in=cust3)
    if invoice.count() != 0:
        service = ServicesList.objects.filter(client=user_obj)
        for k in service:
            count = 0
            services = {}
            for l in invoice:
                if l.service_item.id == k.id:
                    count = count + 1
            services['service_name'] = k.service_name
            services['count'] = count
            per = round(count * 100 / cust3.count(), 2)
            services['percentage'] = str(per) + '%'
            service_wise_stats.append(services)
    return service_wise_stats


class filter_services(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        first = data['first_date']
        last = data['last_date']
        year, month, date = first.split('-')
        year = int(year)
        month = int(month)
        date = int(date)
        last_year, last_month, last_date = last.split('-')
        last_year = int(last_year)
        last_month = int(last_month)
        last_date = int(last_date)
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj)
        cust3 = PaymentEntry.objects.filter(Q(status='Completed') | Q(status='COMPLETED'),created_date__date__range=(datetime.date(year,month,date), datetime.date(last_year,last_month,last_date)),
                                            Vehicle__in=cust2)
        year_wise_servies = filterservices(cust3,user_obj)
        myJson = {"status": "1", "Services":year_wise_servies}
        return JsonResponse(myJson, safe=False)