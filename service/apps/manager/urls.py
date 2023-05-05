from rest_framework.routers import SimpleRouter

from apps.manager.views.auth import user_views

urlpatterns = []

router = SimpleRouter()

router.register('user', user_views.ManageUserView, basename='manage_user_view')

urlpatterns += router.urls
