from rest_framework import serializers

from apps.product.models.product_models import ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
