from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet

from apps.product.models.product_models import ProductCategory, ProductBrand, ProductAttributeKey
from apps.product.views.management.filters import BrandFilter
from apps.product.views.management.serializers import CategorySerializer, ProductBrandSerializer, AttributeKeySerializer
from drf.auth import ManageAuthenticate
from drf.exceptions import ApiNotFoundError
from drf.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from drf.response import JsonResponse


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

    def _get_brand_instance(self, code):
        if isinstance(code, int):
            instance = self.get_queryset().filter(
                id=code
            ).first()
            return instance
        return self.get_queryset().filter(brand_code=code).first()

    @method_decorator(csrf_exempt, name='dispatch')
    def destroy(self, request, *args, **kwargs):
        instance = self._get_brand_instance(kwargs.get('pk'))
        if instance is None:
            raise ApiNotFoundError('品牌不存在或已被删除')
        instance.status = ProductBrand.BrandStatus.DELETED
        instance.save(update_fields=['status'])
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        update_data = request.data
        print(update_data)
        instance = self._get_brand_instance(kwargs.get('pk'))
        if instance is None:
            raise ApiNotFoundError('品牌不存在')
        update_data['id'] = instance.id
        if str(update_data.get('status')) != str(ProductBrand.BrandStatus.DRAFT):
            update_data['status'] = ProductBrand.BrandStatus.DRAFT
            update_data['version'] = update_data.get('version') + 1
            update_data['json_object'] = self.get_serializer(instance).data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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


class AttributeKeyView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
    商品属性Key
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductAttributeKey.objects.all().order_by('priority')
    serializer_class = AttributeKeySerializer
