from rest_framework import serializers
from .models import PaymentEntry, InvoiceItem,FeesItem,DiscountItem,TaxItem
from customer.models import VehicleInfo,CustomerInfo
from customer.serializers import CustomerInfoSerializer,VehicleInfoSerializer
from service.serializers import ServiceListSerializer


class PaymentEntrySerializer(serializers.ModelSerializer):
    Vehicle = VehicleInfoSerializer()
    class Meta:
        model = PaymentEntry
        fields = (
            'id',
            'status',
            'final_amount',
            'tax_offered',
            'amount_tendered',
            'changed_given',
            'discount_offered',
            'payment_mode',
            'created_date',
            'Vehicle',
        )


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = '__all__'

class TaxItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxItem
        fields = '__all__'

class FeesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeesItem
        fields = '__all__'

class DiscountItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountItem
        fields = '__all__'