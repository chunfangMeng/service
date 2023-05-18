from rest_framework.routers import SimpleRouter

from apps.webapp.views import captcha_views
from apps.webapp.views import cms_views
from apps.webapp.views.address import address_views
from apps.webapp.views.config import config_views
from apps.webapp.views.open import views as open_views

urlpatterns = []

router = SimpleRouter()

router.register('captcha', captcha_views.CaptchaView, basename='captcha_view')
router.register('banner', cms_views.ClientCmsView, basename='client_banner')
router.register('provinces/address', address_views.ProvincesAreaView, basename='provinces_address')
router.register('csrf/token', open_views.CsrfTokenView, basename='csrf_token_view')
router.register('config/currency', config_views.CurrencyView, basename='config_currency_view')

urlpatterns += router.urls
