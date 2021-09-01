from rest_framework import serializers
from .models import PaymentEntry, InvoiceItem,FeesItem,DiscountItem,TaxItem,TestTypeItem,MustHaveItem
from customer.models import VehicleInfo,CustomerInfo
from customer.serializers import CustomerInfoSerializer,VehicleInfoSerializer
from service.serializers import ServiceListSerializer


class PaymentEntrySerializer(serializers.ModelSerializer):
    Vehicle = VehicleInfoSerializer()
    class Meta:
        model = PaymentEntry
        fields = (
            'id',
            'invoice_id',
            'status',
            'final_amount',
            'card_amount',
            'tax_offered',
            'amount_tendered',
            'changed_given',
            'discount_offered',
            'payment_mode',
            'created_date',
            'additional_comments',
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

class TestTypeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestTypeItem
        fields = '__all__'

class MustHaveItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MustHaveItem
        fields = '__all__'