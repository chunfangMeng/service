from rest_framework import serializers

from apps.webapp.models.webapp_models import CurrencyConfig, Country


class CountrySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = Country
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = CurrencyConfig
        fields = '__all__'
        depth = 1
