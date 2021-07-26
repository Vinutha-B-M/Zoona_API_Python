from rest_framework import serializers
from .models import PaymentEntry, InvoiceItem
from customer.models import VehicleInfo,CustomerInfo
from customer.serializers import CustomerInfoSerializer,VehicleInfoSerializer

class PaymentEntrySerializer(serializers.ModelSerializer):
    Vehicle = VehicleInfoSerializer()
    class Meta:
        model = PaymentEntry
        fields = (
            'id',
            'status',
            'created_date',
            'Vehicle',
        )


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
