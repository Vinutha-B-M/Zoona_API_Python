from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import ReceiptContentSerializer, TaxesSerializer, DiscountsSerializer, ServiceListSerializer, \
    DefaultListSerializer, FeesSerializer,CashDiscountSerializer,SquareCredentialSerializer
from .models import ReceiptContent, Taxes, Discounts, ServicesList, Default, Fees,CashDiscount,SquareCredential
from django.http import HttpResponse, JsonResponse
from users.models import UserInfo, UserType
from users.serializers import UserInfoSerializer, UserTypeSerializer

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
            userdata= UserType.objects.get(id=session)
            serializer2= UserTypeSerializer(userdata)
            serializer = ReceiptContentSerializer(content)
            myJson = {"status": "1", "data": serializer.data,"userdata":serializer2.data}
            return JsonResponse(myJson)
        else:
            userdata = UserType.objects.get(id=session)
            serializer2 = UserTypeSerializer(userdata)
            myJson = {"status": "1", "data": "", "userdata":serializer2.data}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)

class update_receipt_content(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        pic = request.FILES.get('company_logo')
        id = data['id']
        address = data['address']
        email = data['email']
        footer_note = data['footer_note']
        if ReceiptContent.objects.filter(id=id).exists():
            content = ReceiptContent.objects.get(id=id)
            if pic != None:
                content.company_logo=pic
                content.image_name = pic
            content.address=address
            content.email=email
            content.footer_note=footer_note
            content.save()
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": ""}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)

class add_receipt_content(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        pic = request.FILES.get('company_logo')
        session = data['id']
        address = data['address']
        email = data['email']
        footer_note = data['footer_note']

        user_info_obj = UserType.objects.get(id=session)

        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)

        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = ReceiptContent.objects.create()
            create.address=address
            if pic != None:
                create.company_logo=pic
                create.image_name = pic
            create.email=email
            create.footer_note=footer_note
            create.client=user_obj
            create.save()
            serializer = ReceiptContentSerializer(create)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)

        else:
            myJson = {"status": "0", "data": "error"}
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
            serializer = DiscountsSerializer(content, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
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
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            serializer = TaxesSerializer(content, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
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
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
        tax_name = data['tax_name']
        visible = data['visible']
        if Taxes.objects.filter(id=id).exists():
            content = Taxes.objects.filter(id=id).update(tax_value=tax_value,tax_name=tax_name,visible=visible)
            myJson = {"status": "1", "data": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
        tax_name = data['tax_name']
        visible = data['visible']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = Taxes.objects.create(tax_value=tax_value,tax_name=tax_name,visible=visible, client=user_obj)
            serializer = TaxesSerializer(create)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            serializer = ServiceListSerializer(content, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
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
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            serializer = DefaultListSerializer(content)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
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
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
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
            myJson = {"status": "1", "data":serializer.data}
            return JsonResponse(myJson)

        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class fees(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if Fees.objects.filter(client=user_obj).exists():
            content = Fees.objects.filter(client=user_obj)
            serializer = FeesSerializer(content, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class delete_fees(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        if Fees.objects.filter(id=id).exists():
            content = Fees.objects.filter(id=id).delete()
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class update_fees(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        id = data['id']
        fees_value = data['fees_value']
        fees_name = data['fees_name']
        visible = data['visible']
        if Fees.objects.filter(id=id).exists():
            content = Fees.objects.filter(id=id).update(fees_value=fees_value,fees_name=fees_name,visible=visible)
            myJson = {"status": "1", "data": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)


class add_fees(APIView):
    def post(self, request):
        # session = request.session.get("user_id")
        # if session:
        data = request.data
        session = data['id']
        fees_value = data['fees_value']
        fees_name = data['fees_name']
        visible = data['visible']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = Fees.objects.create(fees_value=fees_value, fees_name=fees_name, visible=visible, client=user_obj)
            serializer = FeesSerializer(create)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)
    # else:
    #     myJson = {"status": "0", "message": "Login expired"}
    #     return JsonResponse(myJson)

class cash_discount(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if CashDiscount.objects.filter(client=user_obj).exists():
            content = CashDiscount.objects.filter(client=user_obj)
            serializer = CashDiscountSerializer(content, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)

class update_cash_discount(APIView):
    def post(self, request):
        data = request.data
        id = data['id']
        cash_discount_amount = data['cash_discount_amount']
        visible = data['visible']
        if CashDiscount.objects.filter(id=id).exists():
            content = CashDiscount.objects.filter(id=id).update(cash_discount_amount=cash_discount_amount,visible=visible)
            myJson = {"status": "1", "data": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)

class add_cash_discount(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        cash_discount_amount = data['cash_discount_amount']
        visible = data['visible']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            create = CashDiscount.objects.create(cash_discount_amount=cash_discount_amount,
                                         visible=visible, client=user_obj)
            serializer = CashDiscountSerializer(create)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)


class square_credential(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if SquareCredential.objects.filter(client=user_obj).exists():
            content = SquareCredential.objects.filter(client=user_obj)
            serializer = SquareCredentialSerializer(content, many=True)
            myJson = {"status": "1", "data": serializer.data}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "1", "data": ""}
            return JsonResponse(myJson)



class delete_square_credential(APIView):
    def post(self, request):
        data = request.data
        id = data['id']
        if SquareCredential.objects.filter(id=id).exists():
            content = SquareCredential.objects.filter(id=id).delete()
            myJson = {"status": "1", "data": "Success"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)


class update_square_credential(APIView):
    def post(self, request):
        data = request.data
        id = data['id']
        application_id = data['application_id']
        application_secret = data['application_secret']
        location_id = data['location_id']
        accees_token = data['accees_token']
        if SquareCredential.objects.filter(id=id).exists():
            content = SquareCredential.objects.filter(id=id).update(application_id=application_id,location_id=location_id,
                                                                    application_secret=application_secret,accees_token=accees_token)
            myJson = {"status": "1", "data": "updated"}
            return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)


class add_square_credential(APIView):
    def post(self, request):
        data = request.data
        session = data['id']
        application_id = data['application_id']
        application_secret = data['application_secret']
        location_id = data['location_id']
        accees_token = data['accees_token']
        user_info_obj = UserType.objects.get(id=session)
        user_obj = UserInfo.objects.get(id=user_info_obj.userinfo.id)
        if UserType.objects.filter(id=session, is_admin=True).exists():
            if SquareCredential.objects.filter(client=user_obj).exists():
                content = SquareCredential.objects.filter(client=user_obj)
                serializer = SquareCredentialSerializer(content, many=True)
                myJson = {"status": "1", "data": serializer.data}
                return JsonResponse(myJson)
            else:
                create = SquareCredential.objects.create(application_id=application_id, application_secret=application_secret,
                                             location_id=location_id, client=user_obj,accees_token=accees_token)
                serializer = SquareCredentialSerializer(create)
                myJson = {"status": "1", "data": serializer.data}
                return JsonResponse(myJson)
        else:
            myJson = {"status": "0", "data": "error"}
            return JsonResponse(myJson)
