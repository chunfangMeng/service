from rest_framework import serializers

from apps.webapp.models.webapp_models import ChinaProvinceArea


class ChinaAddressAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChinaProvinceArea
        fields = '__all__'
