from rest_framework import serializers
from .models import UserInfo, UserType


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = '__all__'


class UserTypeSerializer(serializers.ModelSerializer):

    userinfo = UserInfoSerializer()

    class Meta:
        model = UserType
        fields = (
            'id',
            'username',
            'full_name',
            'phone_number',
            'is_admin',
            'userinfo',
        )
