from rest_framework import serializers
from .models import PaymentEntry, InvoiceItem


class PaymentEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentEntry
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
