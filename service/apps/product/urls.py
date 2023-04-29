from rest_framework.routers import SimpleRouter

from apps.product.views.management import views as product_manage_views

router = SimpleRouter()
urlpatterns = []

router.register('management/category', product_manage_views.ProductCategoryView, basename='product_category_view')
router.register('management/brand', product_manage_views.ProductBrandView, basename='product_brand_view')

urlpatterns += router.urls