from rest_framework import serializers

from apps.member.models import GenderEnum
from apps.manager.models.user_models import ManagerUser


class ManageUserSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    gender = serializers.ChoiceField(
        source='get_gender_display',
        choices=tuple([gender_item.value, gender_item.name] for gender_item in GenderEnum)
    )

    class Meta:
        model = ManagerUser
        fields = '__all__'
