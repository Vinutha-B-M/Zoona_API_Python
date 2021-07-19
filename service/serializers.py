from rest_framework import serializers
from .models import ReceiptContent, Taxes, Discounts, ServicesList, Default


class ReceiptContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptContent
        fields = '__all__'


class TaxesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxes
        fields = '__all__'


class DiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discounts
        fields = '__all__'


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesList
        fields = '__all__'


class DefaultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Default
        fields = '__all__'
