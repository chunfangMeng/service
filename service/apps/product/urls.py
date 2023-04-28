from rest_framework.routers import SimpleRouter

from apps.product.views.management import views as product_manage_views

router = SimpleRouter()
urlpatterns = []

router.register('category', product_manage_views.ProductCategoryView, basename='product_category_view')

urlpatterns += router.urls
