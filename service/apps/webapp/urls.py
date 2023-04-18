from rest_framework.routers import SimpleRouter

from apps.webapp.views.captcha_views import CaptchaView

urlpatterns = []

router = SimpleRouter()

router.register('captcha', CaptchaView, basename='captcha_view')

urlpatterns += router.urls
