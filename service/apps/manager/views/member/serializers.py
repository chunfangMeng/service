from django.contrib.auth.models import User
from rest_framework import serializers

from apps.member.models.user_models import UserMember


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserMember
        fields = '__all__'
