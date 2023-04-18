from rest_framework.routers import SimpleRouter

from apps.member.views.member_views import MemberView


urlpatterns = []

router = SimpleRouter()

router.register('member', MemberView, basename='member_view')

urlpatterns += router.urls
