from user.models import User
from rest_framework import serializers
from integration.models import Integration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id','password','is_superuser','is_staff','date_joined','groups','user_permissions']

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'