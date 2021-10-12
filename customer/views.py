from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

import datetime
import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import CustomerInfoSerializer, VehicleInfoSerializer, TestDetailsSerializer,TermsItemSerializer,SmogTestSerializer
from .models import CustomerInfo, SmogTest, VehicleInfo, TestDetails,TermsItems
from service.models import TermCondition
from users.models import UserInfo, UserType
from rest_framework import viewsets, status
from payment.models import PaymentEntry, InvoiceItem
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# .........................Total-And-New-Customer-Count............................

class Customer(APIView):
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

# .........................END-Total-And-New-Customer-Count............................
# .........................Single-Customer-Info.......................................

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
            serializer2 = TermsItemSerializer(termitems,many=True)
            myJson = {"status": "1", "data": serializer.data,"terms":serializer2.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": ''}
            return JsonResponse(myJson)

# .........................End-Single-Customer-Info.......................................
# .........................Customer-Insert.......................................

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
        estimate_amount = data['estimate_amount']
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
                                                 user_id=user_obj,estimate_amount=estimate_amount)
            for i in terms_item:
                tax_id = i['id']
                term_obj = TermCondition.objects.get(id=tax_id)
                term_text = TermCondition.objects.get(id=tax_id).term_text
                TermsItems.objects.create(terms_text=term_text,term=term_obj,customer=create)
            serializer = CustomerInfoSerializer(create)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)

# .........................END-Customer-Insert.......................................
# .........................Terms-Update-Function.......................................

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

# .........................END-Terms-Update-Function.......................................
# .........................Customer-Update-Info.......................................

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
        estimate_amount = data['estimate_amount']
        postal_code = data['postal_code']
        selected_date = data['selected_date']
        terms_item = data['terms_item']
        customer_exist=CustomerInfo.objects.get(id=session)
        CustomerInfo.objects.filter(id=session).update(company_name=company_name, full_name=full_name,estimate_amount=estimate_amount,
                                                             email_id=email_id,address=address, postal_code=postal_code,
                                                             selected_date=selected_date,
                                                             phone_number=phone_number, address_2=address_2, city=city,
                                                             state=state)
        none_response=term_item_updation(customer_exist,terms_item)
        create=CustomerInfo.objects.get(id=session)
        serializer = CustomerInfoSerializer(create)
        myJson = {"status": "1", "data": serializer.data}
        return JsonResponse(myJson)

# .........................END-Customer-Update-Info.......................................
# .........................Customer-Info-Function.......................................

def customer_info_clientwise(user_obj, cust3,page_no,items_per_page):
    if page_no == -1:
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj,).order_by('id')
        customer_data = []
        for i in customer_obj:
            list = {}
            list_1 = {}
            list_term = []
            d = 0
            for j in cust3:
                list_2 = {}
                if j.customer == i:
                    list_2['term_id'] = j.term.id
                    list_2['term_text'] = j.terms_text
                    list_term.append(list_2)
                    d = d + 1

            list['id'] = i.id
            list['selected_date'] = i.selected_date
            list['company_name'] = i.company_name
            list['full_name'] = i.full_name
            list['email_id'] = i.email_id
            list['address'] = i.address
            list['address_2'] = i.address_2
            list['city'] = i.city
            list['state'] = i.state
            list['phone_number'] = i.phone_number
            list['estimate_amount'] = i.estimate_amount
            list['postal_code'] = i.postal_code
            list['created_date'] = i.created_date
            list['user_id'] = i.user_id.id
            if d != 0:
                list['Terms'] = list_term
            else:
                list['Terms'] = list_term
            customer_data.append(list)
        Customers = []
        Data = {}
        Data['Data'] = customer_data
        Customers.append(Data)
        return Customers
    else:
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj).order_by('id')
        items_per_page = items_per_page
        total_count = customer_obj.count()
        pages = 0
        if total_count > 0:
            pages = total_count / items_per_page
            if pages % 1 == 0:
                pass
            else:
                pages = int(pages)
                pages = pages + 1
        paginator = Paginator(customer_obj, items_per_page)
        page_num = page_no
        pages_data={}
        if pages < page_num:
            pages_data['current_page']=pages
        else:
            pages_data['current_page']=page_num
        if page_num == 1:
            pages_data['Prev']=False
        else:
            pages_data['Prev']=True
        if page_num == pages:
            pages_data['Next']=False
        else:
            pages_data['Next'] = True
        pages_data['total_counts']=total_count
        try:
            customer_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            customer_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            customer_obj = paginator.page(paginator.num_pages)
        customer_data = []
        for i in customer_obj:
            list = {}
            list_1 = {}
            list_term = []
            d = 0
            for j in cust3:
                list_2 = {}
                if j.customer == i:
                    list_2['term_id'] = j.term.id
                    list_2['term_text'] = j.terms_text
                    list_term.append(list_2)
                    d = d + 1

            list['id'] = i.id
            list['selected_date'] = i.selected_date
            list['company_name'] = i.company_name
            list['full_name'] = i.full_name
            list['email_id'] = i.email_id
            list['address'] = i.address
            list['address_2'] = i.address_2
            list['city'] = i.city
            list['state'] = i.state
            list['phone_number'] = i.phone_number
            list['estimate_amount'] = i.estimate_amount
            list['postal_code'] = i.postal_code
            list['created_date'] = i.created_date
            list['user_id'] = i.user_id.id
            if d != 0:
                list['Terms'] = list_term
            else:
                list['Terms'] = list_term
            customer_data.append(list)
        Customers = []
        Customers.append(pages_data)
        Data = {}
        Data['Data'] = customer_data
        Customers.append(Data)
        return Customers
# .........................END-Customer-Info-Function.......................................
# .........................Vehicle-Info-Function.......................................

def vehicle_info_clientwise(cust2, cust3,customer_obj,page_no,items_per_page,cust4):
    if page_no == -1:
        vehicle_data = []
        for k in cust2:
            vehicle = {}
            customer_id = []
            test=0
            smog_list=[]
            for x in cust4:
                    temp_list={}
                    if x.vehicle_id==k:
                       temp_list['smog']=x.smog
                       temp_list['type']=x.type
                       temp_list['desc']=x.desc
                       smog_list.append(temp_list)
            for i in customer_obj:
                list = {}
                list_term = []
                d = 0
                for j in cust3:
                    list_2 = {}
                    if j.customer == i:
                        list_2['term_id'] = j.term.id
                        list_2['term_text'] = j.terms_text
                        list_term.append(list_2)
                        d = d + 1

                if d != 0:
                    list['Terms'] = list_term
                else:
                    list['Terms'] = list_term

                z = 0
                if k.customer_id == i:
                    list_cust = {}
                    z = z + 1
                    vehicle['id'] = k.id
                    vehicle['year'] = k.year
                    vehicle['brand'] = k.brand
                    vehicle['odo_meter'] = k.odo_meter
                    vehicle['vin'] = k.vin
                    vehicle['lic_plate'] = k.lic_plate
                    vehicle['gvwr'] = k.gvwr
                    vehicle['engine'] = k.engine
                    vehicle['engine_group'] = k.engine_group
                    vehicle['cylinder'] = k.cylinder
                    vehicle['Transmission'] = k.Transmission
                    vehicle['brand_model'] = k.brand_model
                    vehicle['smoke_pvc']=k.smoke_pvc
                    vehicle['tailpipe']=k.tailpipe
                    vehicle['smog_test']=smog_list
                    list_cust['id'] = i.id
                    list_cust['selected_date'] = i.selected_date
                    list_cust['company_name'] = i.company_name
                    list_cust['full_name'] = i.full_name
                    list_cust['email_id'] = i.email_id
                    list_cust['address'] = i.address
                    list_cust['address_2'] = i.address_2
                    list_cust['city'] = i.city
                    list_cust['state'] = i.state
                    list_cust['phone_number'] = i.phone_number
                    list_cust['estimate_amount'] = i.estimate_amount
                    list_cust['postal_code'] = i.postal_code
                    list_cust['created_date'] = i.created_date
                    list_cust['user_id'] = i.user_id.id
                    vehicle['customer_id'] = list_cust
                    vehicle['customer_id']['Terms'] = list_term
                if z != 0:
                    vehicle_data.append(vehicle)
        Vehicles = []
        Data = {}
        Data['Data'] = vehicle_data
        Vehicles.append(Data)
        return Vehicles

    else:
        items_per_page = items_per_page
        total_count = cust2.count()
        pages = 0
        if total_count > 0:
            pages = total_count / items_per_page
            if pages % 1 == 0:
                pass
            else:
                pages = int(pages)
                pages = pages + 1
        paginator = Paginator(cust2, items_per_page)
        page_num = page_no
        pages_data = {}
        if pages < page_num:
            pages_data['current_page'] = pages
        else:
            pages_data['current_page'] = page_num
        if page_num == 1:
            pages_data['Prev']=False
        else:
            pages_data['Prev']=True
        if page_num == pages:
            pages_data['Next']=False
        else:
            pages_data['Next'] = True
        pages_data['total_counts'] = total_count
        try:
            cust2 = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            cust2 = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            cust2 = paginator.page(paginator.num_pages)
        vehicle_data = []
        for k in cust2:
            vehicle = {}
            customer_id = []
            for i in customer_obj:
                list = {}
                list_term = []
                d = 0
                for j in cust3:
                    list_2 = {}
                    if j.customer == i:
                        list_2['term_id'] = j.term.id
                        list_2['term_text'] = j.terms_text
                        list_term.append(list_2)
                        d = d + 1

                if d != 0:
                    list['Terms'] = list_term
                else:
                    list['Terms'] = list_term

                z = 0
                if k.customer_id == i:
                    list_cust = {}
                    z = z + 1
                    vehicle['id'] = k.id
                    vehicle['year'] = k.year
                    vehicle['brand'] = k.brand
                    vehicle['odo_meter'] = k.odo_meter
                    vehicle['vin'] = k.vin
                    vehicle['lic_plate'] = k.lic_plate
                    vehicle['gvwr'] = k.gvwr
                    vehicle['engine'] = k.engine
                    vehicle['engine_group'] = k.engine_group
                    vehicle['cylinder'] = k.cylinder
                    vehicle['Transmission'] = k.Transmission
                    vehicle['brand_model'] = k.brand_model
                    vehicle['smoke_pvc']=k.smoke_pvc
                    vehicle['tailpipe']=k.tailpipe
                    list_cust['id'] = i.id
                    list_cust['selected_date'] = i.selected_date
                    list_cust['company_name'] = i.company_name
                    list_cust['full_name'] = i.full_name
                    list_cust['email_id'] = i.email_id
                    list_cust['address'] = i.address
                    list_cust['address_2'] = i.address_2
                    list_cust['city'] = i.city
                    list_cust['state'] = i.state
                    list_cust['phone_number'] = i.phone_number
                    list_cust['estimate_amount'] = i.estimate_amount
                    list_cust['postal_code'] = i.postal_code
                    list_cust['created_date'] = i.created_date
                    list_cust['user_id'] = i.user_id.id
                    vehicle['customer_id'] = list_cust
                    vehicle['customer_id']['Terms'] = list_term
                if z != 0:
                    vehicle_data.append(vehicle)
        Vehicles=[]
        Vehicles.append(pages_data)
        Data={}
        Data['Data']=vehicle_data
        Vehicles.append(Data)
        return Vehicles
# .........................End-Vehicle-Info-Function.......................................

# .........................Vehicle-Info......................................

class Vehicle_List(APIView):

    def post(self, request):
        data = request.data
        session = data['id']
        page_no = data['page_number']
        items_per_page = data['items_per_page']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(customer_id__in=customer_obj).order_by('id')
        cust3 = TermsItems.objects.filter(customer__in=customer_obj)
        cust4 = SmogTest.objects.filter(vehicle_id__in=cust2)
        vehicle_data = vehicle_info_clientwise(cust2, cust3, customer_obj,page_no,items_per_page,cust4)
        myJson = {"status": "1","vehicle_info":vehicle_data}
        return JsonResponse(myJson)

# .........................END-Vehicle-Info......................................
# .........................Customer-Info......................................

class customer_list(APIView):

    def post(self, request):
        data = request.data
        session = data['id']
        page_no = data['page_number']
        items_per_page = data['items_per_page']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust3 = TermsItems.objects.filter(customer__in=customer_obj)
        customer_data= customer_info_clientwise(user_obj,cust3,page_no,items_per_page)
        myJson = {"status": "1","customer_info":customer_data}
        return JsonResponse(myJson)

# .........................END-Customer-Info......................................
# .........................Vehicle-Insert......................................

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
        smog_test = data['smog_test']
        state=data['state']
        tailpipe=data['tailpipe']
        smoke_pvc=data['smoke_pvc']
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
                                                    engine=engine,state=state,tailpipe=tailpipe,smoke_pvc=smoke_pvc,
                                                    cylinder=cylinder, Transmission=Transmission,
                                                    engine_group=engine_group)
                serializer = VehicleInfoSerializer(create)
                vehicle_obj = VehicleInfo.objects.get(id=create.id)
                for i in smog_test:
                    smog = i['smog']
                    type = i['type']
                    desc = i['desc']
                    SmogTest.objects.create(smog=smog, type=type,desc=desc, vehicle_id=vehicle_obj) 
                myJson = {"status": "1", "data": serializer.data}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data":"login_error"}
            return JsonResponse(myJson)
# .........................END-Vehicle-Insert......................................
# .........................Vehicle-Info-Update......................................
def smogtest_update(vehicle_id,smogtest):
    vehicle_obj = VehicleInfo.objects.get(id=vehicle_id)
    for i in smogtest:
        smog = i['smog']
        type = i['type']
        desc = i['desc']
        if SmogTest.objects.filter(smog=smog, vehicle_id=vehicle_obj):
            SmogTest.objects.filter(smog=smog).update(type=type,desc=desc)
        else:
            SmogTest.objects.create(smog=smog, type=type,desc=desc, vehicle_id=vehicle_obj)

    updated_list = SmogTest.objects.filter(vehicle_id=vehicle_obj).values_list('smog', flat=True)
    for i in updated_list:
        dt = 0
        for j in smogtest:
            if j['smog'] == i:
                dt = dt + 1
        if dt == 0:
            SmogTest.objects.filter(smog=i).delete()


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
        smog_test = data['smog_test']
        state = data['state']
        tailpipe=data['tailpipe']
        smoke_pvc=data['smoke_pvc']
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
                                                                     vin=vin, engine=engine,tailpipe=tailpipe,smoke_pvc=smoke_pvc,
                                                                     cylinder=cylinder, Transmission=Transmission,
                                                                     engine_group=engine_group,state=state)
                    create = VehicleInfo.objects.get(id=vehicle_id)
                    serializer = VehicleInfoSerializer(create)
                    smogtest_update(vehicle_id,smog_test)
                    myJson = {"status": "1", "data": serializer.data}
                    return JsonResponse(myJson)
                elif VehicleInfo.objects.filter(customer_id__in=customer_obj_list,vin=vin).exists():
                    myJson = {"status": "0", "data": "VIN Exists"}
                    return JsonResponse(myJson)
                else:
                    VehicleInfo.objects.filter(id=vehicle_id).update(year=year, brand=brand, brand_model=brand_model,
                                                                     odo_meter=odo_meter, lic_plate=lic_plate,
                                                                     gvwr=gvwr,state=state,tailpipe=tailpipe,smoke_pvc=smoke_pvc,
                                                                     vin=vin, engine=engine,
                                                                     cylinder=cylinder, Transmission=Transmission,
                                                                     engine_group=engine_group)
                    create = VehicleInfo.objects.get(id=vehicle_id)
                    serializer = VehicleInfoSerializer(create)
                    smogtest_update(vehicle_id,smog_test)
                    myJson = {"status": "1", "data": serializer.data}
                    return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": "Login_error"}
            return JsonResponse(myJson)

# .........................END-Vehicle-Info-Update......................................


# .........................Customer-Search-Function......................................

def customer_filter_clientwise(user_obj, cust3,keyword,page_no,items_per_page):
    if page_no == -1:
        customer_obj = CustomerInfo.objects.filter(
            Q(company_name__istartswith=keyword) | Q(full_name__istartswith=keyword) |
            Q(email_id__istartswith=keyword) | Q(address__istartswith=keyword) |
            Q(phone_number__startswith=keyword), user_id=user_obj).order_by('id')
        customer_data = []
        for i in customer_obj:
            list = {}
            list_1 = {}
            list_term = []
            d = 0
            for j in cust3:
                list_2 = {}
                if j.customer == i:
                    list_2['term_id'] = j.term.id
                    list_2['term_text'] = j.terms_text
                    list_term.append(list_2)
                    d = d + 1

            list['id'] = i.id
            list['selected_date'] = i.selected_date
            list['company_name'] = i.company_name
            list['full_name'] = i.full_name
            list['email_id'] = i.email_id
            list['address'] = i.address
            list['address_2'] = i.address_2
            list['city'] = i.city
            list['state'] = i.state
            list['phone_number'] = i.phone_number
            list['estimate_amount'] = i.estimate_amount
            list['postal_code'] = i.postal_code
            list['created_date'] = i.created_date
            list['user_id'] = i.user_id.id
            if d != 0:
                list['Terms'] = list_term
            else:
                list['Terms'] = list_term
            customer_data.append(list)

        Customers = []
        Data = {}
        Data['Data'] = customer_data
        Customers.append(Data)
        return Customers
    else:
        customer_obj = CustomerInfo.objects.filter(
            Q(company_name__istartswith=keyword) | Q(full_name__istartswith=keyword) |
            Q(email_id__istartswith=keyword) | Q(address__istartswith=keyword) |
            Q(phone_number__startswith=keyword),user_id=user_obj).order_by('id')
        items_per_page = items_per_page
        total_count = customer_obj.count()
        pages = 0
        if total_count > 0:
            pages = total_count / items_per_page
            if pages % 1 == 0:
                pages=int(pages)
            else:
                pages = int(pages)
                pages = pages + 1
        paginator = Paginator(customer_obj, items_per_page)
        page_num = page_no
        pages_data={}
        if pages < page_num:
            pages_data['current_page']=pages
        else:
            pages_data['current_page']=page_num
        if page_num == 1:
            pages_data['Prev']=False
        else:
            pages_data['Prev']=True
        if page_num == pages:
            pages_data['Next']=False
        elif pages == 0:
            pages_data['Next'] = False
        else:
            pages_data['Next'] = True
        pages_data['total_counts']=total_count
        try:
            customer_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            customer_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            customer_obj = paginator.page(paginator.num_pages)
        customer_data = []
        for i in customer_obj:
            list = {}
            list_1 = {}
            list_term = []
            d = 0
            for j in cust3:
                list_2 = {}
                if j.customer == i:
                    list_2['term_id'] = j.term.id
                    list_2['term_text'] = j.terms_text
                    list_term.append(list_2)
                    d = d + 1

            list['id'] = i.id
            list['selected_date'] = i.selected_date
            list['company_name'] = i.company_name
            list['full_name'] = i.full_name
            list['email_id'] = i.email_id
            list['address'] = i.address
            list['address_2'] = i.address_2
            list['city'] = i.city
            list['state'] = i.state
            list['phone_number'] = i.phone_number
            list['estimate_amount'] = i.estimate_amount
            list['postal_code'] = i.postal_code
            list['created_date'] = i.created_date
            list['user_id'] = i.user_id.id
            if d != 0:
                list['Terms'] = list_term
            else:
                list['Terms'] = list_term
            customer_data.append(list)
        Customers = []
        Customers.append(pages_data)
        Data = {}
        Data['Data'] = customer_data
        Customers.append(Data)
        return Customers
# .........................End-Customer-Search-Function......................................

# .........................Customer-Search......................................
class customers_filter(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        page_no = data['page_number']
        items_per_page = data['items_per_page']
        keyword= data['keyword']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust3 = TermsItems.objects.filter(customer__in=customer_obj)
        customer_data= customer_filter_clientwise(user_obj,cust3,keyword,page_no,items_per_page)
        myJson = {"status": "1","customer_info":customer_data}
        return JsonResponse(myJson)
# .........................End-Customer-Search......................................

# .........................Vehicle-Search-Function......................................
def vehicle_filter_clientwise(cust2, cust3,customer_obj,page_no,items_per_page):
    if page_no == -1:
        vehicle_data = []
        for k in cust2:
            vehicle = {}
            customer_id = []
            for i in customer_obj:
                list = {}
                list_term = []
                d = 0
                for j in cust3:
                    list_2 = {}
                    if j.customer == i:
                        list_2['term_id'] = j.term.id
                        list_2['term_text'] = j.terms_text
                        list_term.append(list_2)
                        d = d + 1

                if d != 0:
                    list['Terms'] = list_term
                else:
                    list['Terms'] = list_term

                z = 0
                if k.customer_id == i:
                    list_cust = {}
                    z = z + 1
                    vehicle['id'] = k.id
                    vehicle['year'] = k.year
                    vehicle['brand'] = k.brand
                    vehicle['odo_meter'] = k.odo_meter
                    vehicle['vin'] = k.vin
                    vehicle['lic_plate'] = k.lic_plate
                    vehicle['gvwr'] = k.gvwr
                    vehicle['engine'] = k.engine
                    vehicle['engine_group'] = k.engine_group
                    vehicle['cylinder'] = k.cylinder
                    vehicle['Transmission'] = k.Transmission
                    vehicle['brand_model'] = k.brand_model
                    list_cust['id'] = i.id
                    list_cust['selected_date'] = i.selected_date
                    list_cust['company_name'] = i.company_name
                    list_cust['full_name'] = i.full_name
                    list_cust['email_id'] = i.email_id
                    list_cust['address'] = i.address
                    list_cust['address_2'] = i.address_2
                    list_cust['city'] = i.city
                    list_cust['state'] = i.state
                    list_cust['phone_number'] = i.phone_number
                    list_cust['estimate_amount'] = i.estimate_amount
                    list_cust['postal_code'] = i.postal_code
                    list_cust['created_date'] = i.created_date
                    list_cust['user_id'] = i.user_id.id
                    vehicle['customer_id'] = list_cust
                    vehicle['customer_id']['Terms'] = list_term
                if z != 0:
                    vehicle_data.append(vehicle)
        Vehicles = []
        Data = {}
        Data['Data'] = vehicle_data
        Vehicles.append(Data)
        return Vehicles

    else:
        items_per_page = items_per_page
        total_count = cust2.count()
        pages = 0
        if total_count > 0:
            pages = total_count / items_per_page
            if pages % 1 == 0:
                pass
            else:
                pages = int(pages)
                pages = pages + 1
        paginator = Paginator(cust2, items_per_page)
        page_num = page_no
        pages_data = {}
        if pages < page_num:
            pages_data['current_page'] = pages
        else:
            pages_data['current_page'] = page_num
        if page_num == 1:
            pages_data['Prev']=False
        else:
            pages_data['Prev']=True
        if page_num == pages:
            pages_data['Next']=False
        else:
            pages_data['Next'] = True
        pages_data['total_counts'] = total_count
        try:
            cust2 = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            cust2 = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            cust2 = paginator.page(paginator.num_pages)
        vehicle_data = []
        for k in cust2:
            vehicle = {}
            customer_id = []
            for i in customer_obj:
                list = {}
                list_term = []
                d = 0
                for j in cust3:
                    list_2 = {}
                    if j.customer == i:
                        list_2['term_id'] = j.term.id
                        list_2['term_text'] = j.terms_text
                        list_term.append(list_2)
                        d = d + 1

                if d != 0:
                    list['Terms'] = list_term
                else:
                    list['Terms'] = list_term

                z = 0
                if k.customer_id == i:
                    list_cust = {}
                    z = z + 1
                    vehicle['id'] = k.id
                    vehicle['year'] = k.year
                    vehicle['brand'] = k.brand
                    vehicle['odo_meter'] = k.odo_meter
                    vehicle['vin'] = k.vin
                    vehicle['lic_plate'] = k.lic_plate
                    vehicle['gvwr'] = k.gvwr
                    vehicle['engine'] = k.engine
                    vehicle['engine_group'] = k.engine_group
                    vehicle['cylinder'] = k.cylinder
                    vehicle['Transmission'] = k.Transmission
                    vehicle['brand_model'] = k.brand_model
                    list_cust['id'] = i.id
                    list_cust['selected_date'] = i.selected_date
                    list_cust['company_name'] = i.company_name
                    list_cust['full_name'] = i.full_name
                    list_cust['email_id'] = i.email_id
                    list_cust['address'] = i.address
                    list_cust['address_2'] = i.address_2
                    list_cust['city'] = i.city
                    list_cust['state'] = i.state
                    list_cust['phone_number'] = i.phone_number
                    list_cust['estimate_amount'] = i.estimate_amount
                    list_cust['postal_code'] = i.postal_code
                    list_cust['created_date'] = i.created_date
                    list_cust['user_id'] = i.user_id.id
                    vehicle['customer_id'] = list_cust
                    vehicle['customer_id']['Terms'] = list_term
                if z != 0:
                    vehicle_data.append(vehicle)
        Vehicles = []
        Vehicles.append(pages_data)
        Data = {}
        Data['Data'] = vehicle_data
        Vehicles.append(Data)
        return Vehicles
# .........................End-Vehicle-Search-Function......................................

# .........................Vehicle-Search......................................

class vehicle_filter(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        page_no = data['page_number']
        items_per_page = data['items_per_page']
        keyword = data['keyword']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        customer_obj = CustomerInfo.objects.filter(user_id=user_obj)
        cust2 = VehicleInfo.objects.filter(Q(customer_id__phone_number__istartswith=keyword) | Q(customer_id__full_name__istartswith=keyword)|
                                           Q(brand__istartswith=keyword) |  Q(year__istartswith=keyword) | Q(vin__istartswith=keyword) ,
                                           customer_id__in=customer_obj).order_by('id')
        cust3 = TermsItems.objects.filter(customer__in=customer_obj)
        vehicle_data = vehicle_filter_clientwise(cust2, cust3, customer_obj,page_no,items_per_page)
        myJson = {"status": "1", "vehicle_info": vehicle_data}
        return JsonResponse(myJson)

# .........................End-Vehicle-Search......................................

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

# .........................Vehicle-Info-Thrid-Party_API......................................

class vehicle_info(APIView):

    def post(self, request):
        data = request.data
        vinField = data['vinField']
        response = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/' + vinField + '?format=json')
        # response = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/' + vinField + '?format=json')
        json_response = response.json()
        return JsonResponse(json_response, safe=False)

# .........................END-Vehicle-Info-Thrid-Party_API......................................