from django.db import models

from apps.webapp.models.abstract_models import TimeStampAbstract, OperatorAbstract


class ProductCategory(TimeStampAbstract, OperatorAbstract):
    """
    商品分类
    """
    class StatusChoices(models.IntegerChoices):
        INIT = 0
        DRAFT = 1
        ONLINE = 2
        DELETED = 3
    name = models.CharField(max_length=64, db_index=True, help_text="分类名称")
    en_name = models.CharField(max_length=128, help_text="英文分类名")
    status = models.IntegerField(default=StatusChoices.INIT, choices=StatusChoices.choices, help_text="状态")
    priority = models.IntegerField(default=0, help_text="优先权")

    class Meta:
        db_table = 'product_category'
        verbose_name = 'ProductCategory'

    def __str__(self):
        return f'{self.name} - {self.en_name}'


class ProductBrand(TimeStampAbstract, OperatorAbstract):
    """
    商品品牌
    """
    class BrandStatus(models.IntegerChoices):
        INIT = 0
        DRAFT = 1
        ONLINE = 2
        DELETED = 3
    name = models.CharField(max_length=32, db_index=True, help_text="商品品牌")
    en_name = models.CharField(max_length=48, help_text="英文品牌")
    status = models.IntegerField(default=BrandStatus.INIT, choices=BrandStatus.choices, help_text="状态")
    logo = models.CharField(max_length=120, null=True, blank=True, help_text="品牌LOGO URL")
    info = models.CharField(max_length=256, null=True, blank=True, help_text="品牌信息")
    priority = models.IntegerField(default=0, help_text="优先权")

    def __str__(self):
        return f'{self.name} - {self.en_name}'

    class Meta:
        db_table = 'product_brand'
        verbose_name = 'ProductBrand'


class StockStatusChoices(models.IntegerChoices):
    AVAILABLE = 0  # 可用
    UNAVAILABLE = 1  # 不可用
    DELETED = 2  # 已删除


class ProductAttributeKey(TimeStampAbstract, OperatorAbstract):
    """
    商品属性Key
    """
    code = models.CharField(max_length=32, unique=True, help_text="属性key代码")
    name = models.CharField(max_length=32, help_text="属性名称")
    priority = models.IntegerField(default=0, help_text="优先权")
    status = models.IntegerField(default=StockStatusChoices.AVAILABLE,
                                 choices=StockStatusChoices.choices, help_text="状态")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, help_text="分类")

    class Meta:
        db_table = 'product_attribute_key'
        unique_together = ('code', 'name')
        verbose_name = 'ProductAttributeKey'

    def __str__(self):
        return f'{self.name}: {self.info}'


class ProductAttributeValue(TimeStampAbstract, OperatorAbstract):
    """商品属性值"""
    attribute_key = models.ForeignKey(ProductAttributeKey, on_delete=models.CASCADE, help_text="属性key")
    value_code = models.CharField(max_length=32, unique=True, help_text="属性值代码")
    attr_value = models.CharField(max_length=48, help_text="属性值")
    priority = models.IntegerField(default=0, help_text="优先权")
    status = models.IntegerField(
        default=StockStatusChoices.AVAILABLE,
        choices=StockStatusChoices.choices, help_text="状态"
    )

    class Meta:
        db_table = 'product_attribute_value'
        unique_together = ('value_code', 'attr_value')
        verbose_name = 'ProductAttributeValue'

    def __str__(self):
        return f'{self.value_code} - {self.attr_value}'


class Product(TimeStampAbstract, OperatorAbstract):
    """
    商品表
    """
    spu_number = models.CharField(max_length=48, help_text="商品编号")
    name = models.CharField(max_length=64, help_text="主名称")
    sub_name = models.CharField(max_length=64, help_text="副名称")
    gross_weight = models.FloatField(default=0, help_text="重量[保留两位小数点]")
    net_weight = models.FloatField(default=0, help_text="净重[保留两位小数点]")
    place_of_origin = models.CharField(max_length=32, help_text="产地")
    item_no = models.CharField(max_length=48, db_index=True, help_text="货号")
    product_brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL,
                                      null=True, blank=True, help_text="商品品牌")

    class Meta:
        db_table = 'Product'
        unique_together = ('spu_number', 'name', 'sub_name')
        verbose_name = 'Product'

    def __str__(self):
        return f'{self.spu_number} - {self.name}'


class ProductRelatedAttribute(TimeStampAbstract, OperatorAbstract):
    """商品关联属性"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="商品")
    product_attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE, help_text="商品属性")

    class Meta:
        db_table = 'product_related_attribute'
        verbose_name = 'ProductRelatedAttribute'

    def __str__(self):
        return f'{self.product} / {self.product_attribute}'


class ProductSpecs(TimeStampAbstract, OperatorAbstract):
    """商品SKU"""
    sku = models.CharField(max_length=24, db_index=True, unique=True, help_text="商品SKU")
    sku_name = models.CharField(max_length=32, help_text="SKU值")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="商品")
    status = models.IntegerField(default=0, choices=StockStatusChoices.choices, help_text="状态")
    priority = models.IntegerField(default=0, help_text="优先权")

    class Meta:
        db_table = 'product_specs'
        verbose_name = 'ProductSpecs'

    def __str__(self):
        return f'{self.sku}:{self.sku_name}/{self.status}'


