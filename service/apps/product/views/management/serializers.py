from rest_framework import serializers

from apps.product.models.product_models import ProductCategory, ProductBrand


class CategorySerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    brand_code = serializers.CharField(read_only=True)
    json_object = serializers.JSONField(write_only=True)
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ProductBrand
        exclude = ('id', )
