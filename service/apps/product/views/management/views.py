from rest_framework.viewsets import GenericViewSet

from apps.product.models.product_models import ProductCategory, ProductBrand
from apps.product.views.management.serializers import CategorySerializer, ProductBrandSerializer
from drf.auth import ManageAuthenticate
from drf.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from drf.response import JsonResponse


class ProductCategoryView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """
    商品分类管理
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductCategory.objects.all()
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


class ProductBrandView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """
    商品品牌管理
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductBrand.objects.all()
    serializer_class = ProductBrandSerializer

