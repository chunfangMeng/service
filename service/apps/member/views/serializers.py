from rest_framework import serializers

from apps.member.models.user_models import UserMember


class MemberSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserMember
        fields = '__all__'
