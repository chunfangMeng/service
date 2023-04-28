from rest_framework.viewsets import GenericViewSet

from apps.product.models.product_models import ProductCategory
from apps.product.views.management.serializers import CategorySerializer
from drf.auth import ManageAuthenticate
from drf.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin


class ProductCategoryView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """
    商品分类
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
