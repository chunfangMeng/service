from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from apps.manager.models import ManagerUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser')


class ManagerStaffSerializer(ModelSerializer):
    user = UserSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = ManagerUser
        fields = '__all__'
