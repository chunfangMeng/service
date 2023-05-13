import tempfile

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
    StockStatusChoices, ProductAttributeValue, Product
from apps.product.views.management.filters import BrandFilter
from apps.product.views.management.serializers import CategorySerializer, ProductBrandSerializer, \
    AttributeGroupSerializer, ProductSerializer
from drf.auth import ManageAuthenticate
from drf.exceptions import ApiNotFoundError
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
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
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
            file_data = excel_handler.read_excel(min_row=1)
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
    """商城"""
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
