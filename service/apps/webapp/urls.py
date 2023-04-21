from rest_framework.routers import SimpleRouter

from apps.webapp.views.captcha_views import CaptchaView
from apps.webapp.views.cms_views import ClientCmsView

urlpatterns = []

router = SimpleRouter()

router.register('captcha', CaptchaView, basename='captcha_view')
router.register('banner', ClientCmsView, basename='client_banner')

urlpatterns += router.urls
