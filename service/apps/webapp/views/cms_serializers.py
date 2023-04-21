from rest_framework import serializers

from apps.webapp.models.cms_models import Banner


class ClientBannerSerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Banner
        fields = '__all__'
