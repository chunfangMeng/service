import re

from django.contrib.auth.models import User, Permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet

from apps.manager.models import ManagerUser
from apps.manager.views.staff.filters import StaffFilter
from apps.manager.views.staff.serializers import ManagerStaffSerializer
from apps.member.models import UserGenderChoices
from drf.auth import ManageAuthenticate
from drf.mixins import ListModelMixin, RetrieveModelMixin
from drf.permission import ManagerPermission, CUSTOM_PERMISSIONS, PERMISSION_GROUP
from drf.response import JsonResponse


class ManagerStaffView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = [ManagerPermission, ]
    queryset = ManagerUser.objects.all().order_by('-id')
    serializer_class = ManagerStaffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StaffFilter
    permission_list = ['staff_view', ]

    @action(methods=['get'], detail=True, permission_list=['staff_change'], url_path='user/permission')
    def get_user_permission(self, request, pk):
        """
        获取用户权限
        :param request:
        :param pk:
        :return:
        """
        all_permission = []
        try:
            user_id = int(pk)
        except ValueError:
            return JsonResponse(code=4043, message='用户ID错误')
        has_permission = []
        manager_user = ManagerUser.objects.filter(
            id=user_id
        ).first()
        for permission in list(manager_user.user.get_user_permissions()):
            has_permission.append(permission.split('.')[-1])
        for group in PERMISSION_GROUP:
            permission_prefix = group[0].split('_group')[0]
            group_obj = {
                'label': group[1],
                'value': group[0],
                'children': []
            }
            for group_item in CUSTOM_PERMISSIONS:
                if group_item[0].find(permission_prefix) != -1:
                    group_obj['children'].append({
                        'label': group_item[1],
                        'value': group_item[0]
                    })
            all_permission.append(group_obj)
        return JsonResponse({
            'all_permission': all_permission,
            'has_permission': has_permission
        })

    @action(methods=['put'], detail=True, permission_list=['staff_change'], url_path='permission/modify')
    def modify_permission(self, request, pk):
        """
        修改用户权限
        :param request:
        :param pk:
        :return:
        """
        permissions = request.data.get('permissions', '')
        try:
            user_id = int(pk)
        except ValueError:
            return JsonResponse(code=4043, message='用户ID错误')
        manager_user = ManagerUser.objects.filter(
            id=user_id
        ).first()
        manager_user.user.user_permissions.clear()
        for permission_key in permissions:
            if permissions.get(permission_key):
                print(permission_key)
                permission_obj = Permission.objects.filter(codename=permission_key.strip()).first()
                if permission_obj:
                    manager_user.user.user_permissions.add(permission_obj)
        manager_user.user.save()
        return JsonResponse(message="权限修改成功")

    @action(methods=['patch'], detail=True, url_path='modify/info')
    def modify_staff_info(self, request, pk):
        """
        修改员工个人信息
        :param request:
        :param pk:
        :return:
        """
        try:
            user_id = int(pk)
        except ValueError:
            return JsonResponse(code=4043, message='用户ID错误')
        manager_user = ManagerUser.objects.filter(
            id=user_id
        ).first()
        if not manager_user:
            return JsonResponse(code=4004, message='员工不存在')
        nickname = request.data.get('nickname')
        phone = request.data.get('phone')
        gender = request.data.get('gender')
        email = request.data.get('user').get('email')
        if len(nickname) > 64:
            return JsonResponse(code=4021, message="昵称长度过长")
        if len(phone) > 24:
            return JsonResponse(code=4021, message="联系电话长度过长")
        if gender not in UserGenderChoices.values:
            return JsonResponse(code=4021, message="性别格式错误")
        rex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(rex, email):
            return JsonResponse(code=4021, message="电子邮箱格式错误")
        manager_user.nickname = nickname
        manager_user.phone = phone
        manager_user.gender = gender
        manager_user.user.email = email
        manager_user.user.save()
        manager_user.save()
        return JsonResponse(message="修改成功")

    @action(methods=['post'], detail=True, url_path='modify/pwd')
    def modify_staff_pwd(self, request, pk):
        password = request.data.get('password')
        try:
            user_id = int(pk)
        except ValueError:
            return JsonResponse(code=4043, message='用户ID错误')
        manager_user = ManagerUser.objects.filter(
            id=user_id
        ).first()
        if not manager_user:
            return JsonResponse(code=4004, message='员工不存在')
        manager_user.user.set_password(password)
        manager_user.user.save()
        return JsonResponse(message='修改成功')
