from rest_framework import serializers

from apps.product.models.product_models import ProductCategory, ProductBrand, ProductAttributeKey, ProductAttributeValue


class CategorySerializer(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_update = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    brand_code = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = ProductBrand
        fields = '__all__'
        extra_kwargs = {
            'brand_code': {
                'error_messages': {
                    'required': '品牌代码不能为空'
                }
            },
            'name': {
                'error_messages': {
                    'required': '品牌名称不能为空'
                }
            },
            'en_name': {
                'error_messages': {
                    'required': '英文品牌名称不能为空'
                }
            }
        }


class AttributeKeySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = ProductAttributeKey
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'
