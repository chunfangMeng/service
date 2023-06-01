from rest_framework.routers import SimpleRouter

from apps.manager.views.auth import user_views
from apps.manager.views.member import member_views
from apps.manager.views.staff import manager_views

urlpatterns = []

router = SimpleRouter()

router.register('user', user_views.ManageUserView, basename='manage_user_view')
router.register('login/log', user_views.UserLoginLogView, basename='user_login_log_view')
router.register('member', member_views.MemberView, basename='manager_member_view')
router.register('staff', manager_views.ManagerStaffView, basename='manager_staff_view')

urlpatterns += router.urls
