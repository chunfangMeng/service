from rest_framework.permissions import BasePermission


CUSTOM_PERMISSIONS = (
    ('staff_group', '员工管理'),
    ('staff_view', '员工查看'),
    ('staff_change', '员工编辑'),
    ('staff_remove', '员工删除'),
    ('staff_add', '员工新增'),
    ('shop_brand_group', '商城品牌'),
    ('shop_brand_add', '品牌新增'),
    ('shop_brand_change', '品牌修改'),
    ('shop_brand_delete', '品牌删除'),
    ('shop_brand_view', '品牌查看'),
    ('shop_brand_export', '品牌导出'),
    ('shop_category_group', '商城分类'),
    ('shop_category_view', '商城分类查看'),
    ('shop_category_change', '商城分类修改'),
    ('shop_category_delete', '商城分类删除'),
    ('shop_category_add', '商城分类新增'),
    ('shop_category_export', '商城分类导出'),
    ('shop_attribute_group', '商城属性组'),
    ('shop_attribute_view', '属性组查看'),
    ('shop_attribute_change', '属性组编辑'),
    ('shop_attribute_delete', '属性组删除'),
    ('shop_attribute_export', '属性组导出'),
    ('shop_product_group', '商城商品'),
    ('shop_product_view', '商品查看'),
    ('shop_product_change', '商品编辑'),
    ('shop_product_delete', '商品删除'),
    ('shop_product_add', '商品新增'),
    ('shop_product_export', '商品导出'),
    ('shop_product_attribute_change', '商品属性设置'),
    ('shop_product_specs_change', '商品价格设置'),
    ('member_group', '会员列表'),
    ('member_view', '会员查看'),
    ('member_all_view', '全会员查看'),
    ('member_change', '会员编辑'),
    ('member_delete', '会员删除'),
    ('member_add', '会员新增'),
    ('member_export', '会员信息导出'),
    ('member_statistics', '会员统计'),
)


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not request.user.is_authenticated:
            return False
        all_permission = list(request.user.get_user_permissions())
        if len(list(set(all_permission).intersection(set(view.permission_list)))) == 0:
            return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False
