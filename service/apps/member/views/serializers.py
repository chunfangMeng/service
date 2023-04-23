from django.contrib.auth.models import User
from rest_framework import serializers

from apps.member.models.user_models import UserMember


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserMember
        fields = '__all__'
