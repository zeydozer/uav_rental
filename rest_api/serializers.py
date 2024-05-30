from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UAV, Rental

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

class UAVSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAV
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    uav = UAVSerializer(read_only = True)
    renting_member = UserSerializer(read_only = True)
    uav_id = serializers.PrimaryKeyRelatedField(queryset=UAV.objects.all(), source='uav')
    renting_member_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='renting_member')
    class Meta:
        model = Rental
        fields = '__all__'