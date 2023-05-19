import tempfile

from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from apps.product.models.product_models import ProductCategory, ProductBrand, ProductAttributeKey, \
    StockStatusChoices, ProductAttributeValue, Product, ProductImage, ProductRelatedAttribute, ProductSpecs
from apps.product.views.management.filters import BrandFilter
from apps.product.views.management.serializers import CategorySerializer, ProductBrandSerializer, \
    AttributeGroupSerializer, ProductSerializer, ProductImageSerializer, ProductSpecsSerializer
from apps.webapp.models import CurrencyConfig
from apps.webapp.views.config.serializers import CurrencySerializer
from drf.auth import ManageAuthenticate
from drf.exceptions import ApiNotFoundError, RequestParamsError
from drf.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from drf.response import JsonResponse
from libs.excel_hanlder import ExcelHandler


class ProductCategoryView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """
    商品分类管理
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductCategory.objects.all().order_by('priority')
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        request_data = request.data
        del request_data['code']
        del request_data['parent_code']
        request_data['last_editor'] = request.user.username
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(serializer.data)


class ProductBrandView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    """
    商品品牌管理
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductBrand.objects.filter(~Q(status=ProductBrand.BrandStatus.DELETED))
    serializer_class = ProductBrandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BrandFilter

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        if isinstance(self.kwargs[lookup_url_kwarg], int):
            obj = get_object_or_404(queryset, **filter_kwargs)
        else:
            obj = queryset.filter(brand_code=self.kwargs[lookup_url_kwarg]).first()
            if obj is None:
                raise ApiNotFoundError('品牌不存在')
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(
            Q(brand_code=kwargs.get('pk')) | Q(id=kwargs.get('pk'))
        ).first()
        if instance is None:
            raise ApiNotFoundError('品牌不存在或已被删除')
        if instance.status == ProductBrand.BrandStatus.DRAFT:
            return JsonResponse(instance.json_object)
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

    @method_decorator(csrf_exempt, name='dispatch')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = ProductBrand.BrandStatus.DELETED
        instance.save(update_fields=['status'])
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        update_data = request.data
        instance = self.get_object()
        update_data['id'] = instance.id
        if str(update_data.get('status')) != str(ProductBrand.BrandStatus.DRAFT):
            update_data['status'] = ProductBrand.BrandStatus.DRAFT
            update_data['version'] = update_data.get('version') + 1
            update_data['json_object'] = self.get_serializer(instance).data
        serializer = self.get_serializer(instance, data=update_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(serializer.data)

    @action(methods=['get'], detail=False)
    def options(self, request):
        return JsonResponse(
            data={
                'status_options': [{
                    'label': item.name,
                    'value': item.value
                } for item in ProductBrand.BrandStatus]
            }
        )

    @action(methods=['post'], detail=False)
    def upload(self, request):
        """
        批量上传，创建或者更新
        :param request:
        :return:
        """
        file_byte = request.FILES.get('files')
        with tempfile.NamedTemporaryFile(suffix=f'.{file_byte.name.split(".")[-1]}') as tmp:
            tmp.write(file_byte.read())
            excel_handler = ExcelHandler(tmp.name)
            file_data, _ = excel_handler.read_excel()
        create_obj_list = []
        update_obj_list = []
        error_list = []
        for item in file_data:
            brand_code, brand_name, brand_en_name, brand_status = item
            if str(brand_code).strip() is None:
                error_list.append('品牌代码不能为空')
            if str(brand_name).strip() is None:
                error_list.append('品牌名称不能为空')
            if str(brand_en_name).strip() is None:
                error_list.append('英文品牌名称不能为空')
            if not str(brand_status).isdigit():
                error_list.append('状态错误')
            if int(brand_status) not in ProductBrand.BrandStatus.values or \
                    int(brand_status) == ProductBrand.BrandStatus.DELETED.value:
                error_list.append('品牌状态不存在')
            brand_obj = self.get_queryset().filter(brand_code=str(item[0])).first()
            if brand_obj is None:
                product_brand = ProductBrand(
                    brand_code=str(item[0]),
                    name=str(item[1]),
                    en_name=str(item[2]),
                    status=int(item[3])
                )
                create_obj_list.append(product_brand)
            else:
                brand_obj.name = str(item[1])
                brand_obj.en_name = str(item[2])
                brand_obj.status = int(item[3])
                update_obj_list.append(
                    brand_obj
                )
        if len(error_list) > 0:
            return JsonResponse(code=425, message='\n'.join(error_list))
        if len(create_obj_list) > 0:
            ProductBrand.objects.bulk_create(create_obj_list)
        if len(update_obj_list) > 0:
            ProductBrand.objects.bulk_update(update_obj_list, fields=['name', 'en_name', 'status'])
        return JsonResponse()


class AttributeGroupView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
    商品属性Key
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductAttributeKey.objects.filter(~Q(status=StockStatusChoices.DELETED.value)).order_by('priority')
    serializer_class = AttributeGroupSerializer

    def _get_attr_group_value(self, request, pk):
        attr_value_code = request.data.get('attr_value_code')
        attr_group_obj = self.get_queryset().filter(id=pk).first()
        instance = ProductAttributeValue.objects.filter(
            Q(attribute_key=attr_group_obj, value_code=attr_value_code) &
            ~Q(status=StockStatusChoices.DELETED.value)
        ).first()
        return instance

    def list(self, request, *args, **kwargs):
        is_show_all = request.GET.get('is_show_all')
        queryset = self.filter_queryset(self.get_queryset())
        if is_show_all:
            return JsonResponse(self.get_serializer(queryset, many=True).data)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)

    @action(methods=['delete'], detail=True, url_path='delete/value')
    def delete_attribute_value(self, request, *args, **kwargs):
        """
        删除属性分组下的属性
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self._get_attr_group_value(request, kwargs.get('pk'))
        if instance is None:
            raise ApiNotFoundError('属性值已被删除')
        instance.status = StockStatusChoices.DELETED.value
        instance.value_code = f'{instance.value_code}_DELETED'
        instance.save(update_fields=['status', 'value_code'])
        return JsonResponse(message='删除成功')

    @action(methods=['patch'], detail=True, url_path='value/status')
    def change_attr_value_status(self, request, *args, **kwargs):
        value_status = request.data.get('status')
        instance = self._get_attr_group_value(request, kwargs.get('pk'))
        if instance.status == value_status:
            return JsonResponse(message='状态不能相同')
        instance.status = value_status
        instance.save(update_fields=['status'])
        return JsonResponse(message='切换状态成功')


class ProductView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """商城商品"""
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['get'], detail=True)
    def image(self, request, *args, **kwargs):
        instance = self.get_object()
        image_list = ProductImage.objects.filter(product=instance)
        product_image = ProductImageSerializer(image_list, many=True)
        return JsonResponse(product_image.data)

    @action(methods=['delete'], detail=True, url_path='unbind/attr')
    def unbind_attr(self, request, *args, **kwargs):
        attr_value_code = request.data.get('attr_value_code', [])
        if not attr_value_code:
            raise RequestParamsError('属性值代码不能为空')
        instance = self.get_object()
        if instance is None:
            raise RequestParamsError('商品已被删除')
        ProductRelatedAttribute.objects.filter(
            product=instance,
            product_attribute_value__value_code__in=attr_value_code
        ).delete()
        return JsonResponse(message='解绑成功')

    @action(methods=['post'], detail=True, url_path='bind/attr')
    def attr_bind(self, request, *args, **kwargs):
        """属性绑定"""
        attr_code = request.data.get('attr_code')
        if not attr_code:
            raise RequestParamsError('属性代码不能为空')
        instance = self.get_object()
        attr_value = ProductAttributeValue.objects.filter(value_code=attr_code).first()
        if not attr_value:
            raise RequestParamsError('属性不存在')
        related_obj = ProductRelatedAttribute.objects.filter(
            product=instance,
            product_attribute_value=attr_value
        ).exists()
        if related_obj:
            raise RequestParamsError('属性已绑定，请勿重复绑定')
        ProductRelatedAttribute.objects.create(
            product=instance,
            product_attribute_value=attr_value
        )
        return JsonResponse(message='绑定成功')

    @action(methods=['get'], detail=True)
    def specs(self, request, *args, **kwargs):
        instance = self.get_object()
        specs_list = ProductSpecs.objects.filter(
            product=instance
        )
        return JsonResponse(ProductSpecsSerializer(specs_list, many=True).data)

    @action(methods=['post'], detail=True, url_path='related/specs')
    def related_specs(self, request, *args, **kwargs):
        body_data = request.data
        body_data['price'] = Decimal(body_data.get('price')).quantize(Decimal('0.00'))
        instance = self.get_object()
        currency_obj = CurrencyConfig.objects.filter(id=body_data.get('currency')).first()
        if not currency_obj:
            raise RequestParamsError('请先选择货币')
        specs_check = ProductSpecs.objects.filter(
            product=instance,
            currency=currency_obj,
            price=body_data.get('price')
        ).exists()
        if specs_check:
            raise RequestParamsError('该商品已设置同样的价格')
        body_data.update({
            'product': instance,
            'founder': request.user.username,
            'currency': currency_obj
        })
        ProductSpecs.objects.create(**body_data)
        return JsonResponse(message='绑定价格成功')

    @action(methods=['delete'], detail=True, url_path='unbind/specs')
    def unbind_specs(self, request, *args, **kwargs):
        specs_id = request.data.get('specs_id')
        if not specs_id:
            raise RequestParamsError('请提交价格ID')
        instance = self.get_object()
        ProductSpecs.objects.filter(
            product=instance,
            id=specs_id
        ).delete()
        return JsonResponse(message='删除成功')

    @action(methods=['put', 'patch'], detail=True, url_path='edit/specs')
    def edit_specs(self, request, *args, **kwargs):
        instance = self.get_object()
        specs_id = request.data.get('id')
        sku_name = request.data.get('sku_name', None)
        price = request.data.get('price', None)
        if not sku_name:
            raise RequestParamsError('SKU名称不能为空')
        if len(sku_name) > 32:
            raise RequestParamsError('SKU名称长度不能超过32位')
        if not specs_id:
            raise RequestParamsError('请提交价格ID')
        if not price:
            raise RequestParamsError('价格不能为空')
        try:
            price = Decimal(str(price)).quantize(Decimal('0.00'))
            assert price > 0
        except InvalidOperation:
            return JsonResponse(code=450, message="价格格式不正确")
        except AssertionError:
            return JsonResponse(code=451, message='价格必须大于0')
        specs_instance = ProductSpecs.objects.filter(
            id=specs_id,
            product=instance,
            price=price
        ).exists()
        if specs_instance:
            raise RequestParamsError(f'{price}价格已存在')
        ProductSpecs.objects.filter(
            id=specs_id,
            product=instance
        ).update(
            sku_name=sku_name,
            price=price,
            last_editor=request.user.username,
        )
        return JsonResponse()
