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
    name = models.CharField(max_length=64, verbose_name="分类名称")
    code = models.CharField(max_length=32, unique=True, verbose_name="分类代码")
    en_name = models.CharField(max_length=128, verbose_name="英文分类名")
    status = models.IntegerField(default=StatusChoices.INIT, choices=StatusChoices.choices, verbose_name="状态")
    priority = models.IntegerField(default=0, verbose_name="优先权")
    parent_code = models.CharField(max_length=32, null=True, blank=True, verbose_name='父级Code')

    class Meta:
        db_table = 'product_category'
        verbose_name = 'ProductCategory'
        unique_together = ('name', 'code')
        ordering = ('priority', 'id')

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
        OFFLINE = 4
    name = models.CharField(max_length=32, db_index=True, verbose_name="商品品牌")
    brand_code = models.CharField(max_length=32, unique=True, verbose_name='品牌代码')
    en_name = models.CharField(max_length=48, verbose_name="英文品牌")
    status = models.IntegerField(default=BrandStatus.INIT, choices=BrandStatus.choices, verbose_name="状态")
    logo = models.CharField(max_length=120, null=True, blank=True, verbose_name="品牌LOGO URL")
    info = models.CharField(max_length=256, null=True, blank=True, verbose_name="品牌信息")
    priority = models.IntegerField(default=0, verbose_name="优先权")
    version = models.IntegerField(default=0, verbose_name="版本号")
    json_object = models.JSONField(null=True, verbose_name="旧版本数据")

    def __str__(self):
        return f'{self.name} - {self.en_name}'

    class Meta:
        db_table = 'product_brand'
        unique_together = ('name', 'brand_code')
        verbose_name = 'ProductBrand'
        ordering = ('priority', 'id')


class StockStatusChoices(models.IntegerChoices):
    AVAILABLE = 0  # 可用
    UNAVAILABLE = 1  # 不可用
    DELETED = 2  # 已删除


class ProductAttributeKey(TimeStampAbstract, OperatorAbstract):
    """
    商品属性Key
    """
    code = models.CharField(max_length=32, unique=True, verbose_name="属性key代码")
    name = models.CharField(max_length=32, verbose_name="属性名称")
    priority = models.IntegerField(default=0, verbose_name="优先权")
    status = models.IntegerField(default=StockStatusChoices.AVAILABLE,
                                 choices=StockStatusChoices.choices, verbose_name="状态")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分类")

    class Meta:
        db_table = 'product_attribute_key'
        unique_together = ('code', 'name')
        verbose_name = 'ProductAttributeKey'
        ordering = ('priority', 'id')

    def __str__(self):
        return f'{self.name}: {self.info}'


class ProductAttributeValue(TimeStampAbstract, OperatorAbstract):
    """商品属性值"""
    attribute_key = models.ForeignKey(ProductAttributeKey, on_delete=models.CASCADE, verbose_name="属性key")
    value_code = models.CharField(max_length=32, unique=True, verbose_name="属性值代码")
    attr_value = models.CharField(max_length=48, verbose_name="属性值")
    priority = models.IntegerField(default=0, verbose_name="优先权")
    status = models.IntegerField(
        default=StockStatusChoices.AVAILABLE,
        choices=StockStatusChoices.choices, verbose_name="状态"
    )

    class Meta:
        db_table = 'product_attribute_value'
        unique_together = ('value_code', 'attr_value')
        verbose_name = 'ProductAttributeValue'
        ordering = ('priority', 'id')

    def __str__(self):
        return f'{self.value_code} - {self.attr_value}'


class Product(TimeStampAbstract, OperatorAbstract):
    """
    商品表
    """
    spu_number = models.CharField(max_length=48, verbose_name="商品编号")
    name = models.CharField(max_length=64, verbose_name="主名称")
    sub_name = models.CharField(max_length=64, verbose_name="副名称")
    gross_weight = models.FloatField(default=0, verbose_name="重量[保留两位小数点]")
    net_weight = models.FloatField(default=0, verbose_name="净重[保留两位小数点]")
    place_of_origin = models.CharField(max_length=32, verbose_name="产地")
    item_no = models.CharField(max_length=48, db_index=True, verbose_name="货号")
    product_brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name="商品品牌")

    class Meta:
        db_table = 'Product'
        unique_together = ('spu_number', 'name', 'sub_name')
        verbose_name = 'Product'
        ordering = ('-id', )

    def __str__(self):
        return f'{self.spu_number} - {self.name}'


class ProductRelatedAttribute(TimeStampAbstract, OperatorAbstract):
    """商品关联属性"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    product_attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE, verbose_name="商品属性")

    class Meta:
        db_table = 'product_related_attribute'
        verbose_name = 'ProductRelatedAttribute'

    def __str__(self):
        return f'{self.product} / {self.product_attribute}'


class ProductSpecs(TimeStampAbstract, OperatorAbstract):
    """商品SKU"""
    sku = models.CharField(max_length=24, db_index=True, unique=True, verbose_name="商品SKU")
    sku_name = models.CharField(max_length=32, verbose_name="SKU值")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    status = models.IntegerField(default=0, choices=StockStatusChoices.choices, verbose_name="状态")
    priority = models.IntegerField(default=0, verbose_name="优先权")

    class Meta:
        db_table = 'product_specs'
        verbose_name = 'ProductSpecs'
        ordering = ('priority', '-id')

    def __str__(self):
        return f'{self.sku}:{self.sku_name}/{self.status}'


