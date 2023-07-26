from rest_framework import serializers
from .models import CustomerInfo, SmogTest, VehicleInfo, TestDetails,TermsItems


class CustomerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerInfo
        fields = '__all__'


class VehicleInfoSerializer(serializers.ModelSerializer):
    customer_id = CustomerInfoSerializer()

    class Meta:
        model = VehicleInfo
        fields = (
            'id',
            'year',
            'brand',
            'odo_meter',
            'vin',
            'lic_plate',
            'gvwr',
            'engine',
            'engine_group',
            'cylinder',
            'Transmission',
            'brand_model',
            'state',
            'status',
            'vehicle_signature',
            'tailpipe',
            'smoke_pvc',
            'created_date',
            'customer_id',
        )



class TestDetailsSerializer(serializers.ModelSerializer):
    vehicle_id = VehicleInfoSerializer()

    class Meta:
        model = TestDetails
        fields = (
            'id',
            'vehicle_id',
            'selected_date',
        )


class TermsItemSerializer(serializers.ModelSerializer):
    customer = CustomerInfoSerializer()
    class Meta:
        model = TermsItems
        fields =  (
            'id',
            'terms_text',
            'term',
            'customer',
        )

class SmogTestSerializer(serializers.ModelSerializer):
    vehicle_id = VehicleInfoSerializer()
    class Meta:
        model = SmogTest
        fields = (
            'smog',
            'type',
            'desc',
            'vehicle_id',
        )
