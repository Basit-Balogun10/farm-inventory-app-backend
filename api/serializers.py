from rest_framework import serializers
from .models import Account, Broiler, InventoryWeek, Notification
from django.conf import settings
from django.conf import settings
from rest_framework.authtoken.views import Token


class BroilerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=Account.objects.all(), slug_field='email')

    class Meta:
        model = Broiler
        fields = ['id', 'weight', 'feed', 'temperature', 'animal_bedding', 'user']
        

class InventoryWeekSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=InventoryWeek.objects.all(), slug_field='email')

    class Meta:
        model = Broiler
        fields = ['broilers', 'is_concluded', 'user']
        

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=Notification.objects.all(), slug_field='email')

    class Meta:
        model = Notification
        fields = ['text', 'is_read', 'user']


class UserSerializer(serializers.ModelSerializer):
    broilers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'firstname', 'lastname', 'organization_name', 'password', 'broilers']

        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
