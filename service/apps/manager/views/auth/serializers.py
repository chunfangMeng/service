from rest_framework import serializers

from apps.manager.models.user_models import ManagerUser, UserLoginLog
from apps.member.models import UserGenderChoices


class ManageUserSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    gender = serializers.ChoiceField(
        source='get_gender_display',
        choices=UserGenderChoices.choices
    )

    class Meta:
        model = ManagerUser
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLoginLog
        fields = '__all__'
