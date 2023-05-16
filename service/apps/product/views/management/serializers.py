from django.db.models import Q, Count
from rest_framework import serializers

from apps.product.models.product_models import ProductCategory, ProductBrand, ProductAttributeKey, \
    ProductAttributeValue, StockStatusChoices, Product, ProductRelatedAttribute, ProductImage


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
    # 属性值

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class AttributeGroupSerializer(serializers.ModelSerializer):
    # 属性组
    category = CategorySerializer()
    attr_values = serializers.SerializerMethodField(read_only=True)

    def get_attr_values(self, obj):
        group_query = ProductAttributeValue.objects.filter(
            Q(attribute_key=obj) & ~Q(status=StockStatusChoices.DELETED.value)
        )
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


class ProductAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRelatedAttribute
        fields = ('product', 'product_attribute_value')
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    attr_group = serializers.SerializerMethodField()

    def get_attr_group(self, instance):
        all_attr_key = ProductAttributeKey.objects.all()
        all_attr_group = []
        for attr_key in all_attr_key:
            related_attribute = ProductRelatedAttribute.objects.filter(
                product=instance,
                product_attribute_value__attribute_key=attr_key
            ).values('product_attribute_value__attribute_key_id').first()
            attribute_obj = ProductAttributeKey.objects.filter(
                id=related_attribute.get('product_attribute_value__attribute_key_id')
            ).first()
            all_attr_group.append(AttributeGroupSerializer(attribute_obj).data)
        return all_attr_group

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['create_at'] = instance.create_at.strftime('%Y-%m-%d %H:%M:%S')
        data['last_update'] = instance.last_update.strftime('%Y-%m-%d %H:%M:%S')
        return data

    class Meta:
        model = Product
        fields = ('id', 'spu_number', 'name', 'sub_name', 'gross_weight', 'net_weight', 'place_of_origin', 'item_no',
                  'priority', 'product_brand', 'create_at', 'last_update', 'founder', 'last_editor', 'attr_group')
        depth = 1


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

