from rest_framework.routers import SimpleRouter

from apps.webapp.views import captcha_views
from apps.webapp.views import cms_views
from apps.webapp.views.address import address_views

urlpatterns = []

router = SimpleRouter()

router.register('captcha', captcha_views.CaptchaView, basename='captcha_view')
router.register('banner', cms_views.ClientCmsView, basename='client_banner')
router.register('provinces/address', address_views.ProvincesAreaView, basename='provinces_address')

urlpatterns += router.urls
