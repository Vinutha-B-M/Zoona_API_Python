from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import ReceiptContentSerializer, TaxesSerializer, DiscountsSerializer, ServiceListSerializer, \
    DefaultListSerializer
from .models import ReceiptContent, Taxes, Discounts, ServicesList, Default
from django.http import HttpResponse, JsonResponse
from users.models import UserInfo, UserType


# Create your views here.
class receipt_content(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if ReceiptContent.objects.filter(client=user_obj).exists():
            content = ReceiptContent.objects.get(client=user_obj)
            obj = ReceiptContentSerializer(content)
            return Response(obj.data)
        else:
            myJson = {"status": "1", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)

class update_receipt_content(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        company_name = data['company_name']
        address = data['address']
        phone_number = data['phone_number']
        website_url = data['website_url']
        footer_note = data['footer_note']
        if ReceiptContent.objects.filter(id=id).exists():
            content = ReceiptContent.objects.filter(id=id).update(company_name=company_name,address=address,
                                                                  phone_number=phone_number,website_url=website_url,
                                                                  footer_note=footer_note)
            myJson = {"status": "1", "message": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)

class add_receipt_content(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        data = request.data
        company_name = data['company_name']
        address = data['address']
        phone_number = data['phone_number']
        website_url = data['website_url']
        footer_note = data['footer_note']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)

        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = ReceiptContent.objects.create(company_name=company_name, address=address,
                                                   phone_number=phone_number,
                                                   website_url=website_url, footer_note=footer_note, client=user_obj)
            serializer = ReceiptContentSerializer(create)
            return Response(serializer.data)

        else:
            myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class discounts(APIView):

    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if Discounts.objects.filter(client=user_obj).exists():
            content = Discounts.objects.filter(client=user_obj)
            obj = DiscountsSerializer(content, many=True)
            return Response(obj.data)
        else:
            myJson = {"status": "1", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class delete_discounts(APIView):

    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        if Discounts.objects.filter(id=id).exists():
            content = Discounts.objects.filter(id=id).delete()
            myJson = {"status": "1", "message": "deleted"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class update_discounts(APIView):

    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        discount_value = data['discount_value']
        offer_name = data['offer_name']
        if Discounts.objects.filter(id=id).exists():
            content = Discounts.objects.filter(id=id).update(discount_value=discount_value, offer_name=offer_name)
            myJson = {"status": "1", "message": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class add_discounts(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        discount_value = data['discount_value']
        offer_name = data['offer_name']
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = Discounts.objects.create(discount_value=discount_value, offer_name=offer_name, client=user_obj)
            serializer = DiscountsSerializer(create)
            return Response(serializer.data)
        else:
            myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class taxes(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if Taxes.objects.filter(client=user_obj).exists():
            content = Taxes.objects.filter(client=user_obj)
            obj = TaxesSerializer(content, many=True)
            return Response(obj.data)
        else:
            myJson = {"status": "1", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class delete_taxes(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        if Taxes.objects.filter(id=id).exists():
            content = Taxes.objects.filter(id=id).delete()
            myJson = {"status": "1", "message": "deleted"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class update_taxes(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        tax_value = data['tax_value']
        if Taxes.objects.filter(id=id).exists():
            content = Taxes.objects.filter(id=id).update(tax_value=tax_value)
            myJson = {"status": "1", "message": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class add_taxes(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        tax_value = data['tax_value']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = Taxes.objects.create(tax_value=tax_value, client=user_obj)
            serializer = TaxesSerializer(create)
            return Response(serializer.data)
        else:
            myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class services(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if ServicesList.objects.filter(client=user_obj).exists():
            content = ServicesList.objects.filter(client=user_obj)
            obj = ServiceListSerializer(content, many=True)
            return Response(obj.data)
        else:
            myJson = {"status": "1", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class delete_services(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        if ServicesList.objects.filter(id=id).exists():
            content = ServicesList.objects.filter(id=id).delete()
            myJson = {"status": "1", "message": "deleted"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class update_services(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        service_name = data['service_name']
        input_mode = data['input_mode']
        amount = data['amount']
        if ServicesList.objects.filter(id=id).exists():
            content = ServicesList.objects.filter(id=id).update(service_name=service_name, input_mode=input_mode,
                                                                amount=amount)
            myJson = {"status": "1", "message": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class add_services(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        service_name = data['service_name']
        input_mode = data['input_mode']
        amount = data['amount']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)

        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = ServicesList.objects.create(service_name=service_name, input_mode=input_mode,
                                                 client=user_obj, amount=amount)
            serializer = ServiceListSerializer(create)
            return Response(serializer.data)
        else:
            myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class defaults(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if Default.objects.filter(client=user_obj).exists():
            content = Default.objects.get(client=user_obj)
            obj = DefaultListSerializer(content)
            return Response(obj.data)
        else:
            myJson = {"status": "1", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class update_defaults(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        currency = data['currency']
        langaugge = data['langaugge']
        time_zone = data['time_zone']
        display_time = data['display_time']
        date_format = data['date_format']
        if Default.objects.filter(id=id).exists():
            content = Default.objects.filter(id=id).update(currency=currency,langaugge=langaugge,time_zone=time_zone,
                                                           display_time=display_time,date_format=date_format)
            myJson = {"status": "1", "message": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "message": "no data"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)

class add_defaults(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        currency = data['currency']
        langaugge = data['langaugge']
        time_zone = data['time_zone']
        display_time = data['display_time']
        date_format = data['date_format']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = Default.objects.create(currency=currency, langaugge=langaugge, time_zone=time_zone,
                                            display_time=display_time, date_format=date_format, client=user_obj)
            serializer = DefaultListSerializer(create)
            return Response(serializer.data)

        else:
            myJson = {"status": "0", "message": "Wrong Login/Non admin Login"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)
