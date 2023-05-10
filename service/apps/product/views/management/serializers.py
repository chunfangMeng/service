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


class AttributeValueSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class AttributeGroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    attr_values = serializers.SerializerMethodField()

    def get_attr_values(self, obj):
        group_query = ProductAttributeValue.objects.filter(attribute_key=obj)
        group_data = AttributeValueSerializer(group_query, many=True)
        return group_data.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = ProductAttributeKey
        fields = ('id', 'code', 'name', 'priority', 'status', 'category', 'create_at', 'last_update', 'founder',
                  'last_editor', 'attr_values')

