# Generated by Django 4.1.7 on 2023-04-29 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-id',), 'verbose_name': 'Product'},
        ),
        migrations.AlterModelOptions(
            name='productattributekey',
            options={'ordering': ('priority', 'id'), 'verbose_name': 'ProductAttributeKey'},
        ),
        migrations.AlterModelOptions(
            name='productattributevalue',
            options={'ordering': ('priority', 'id'), 'verbose_name': 'ProductAttributeValue'},
        ),
        migrations.AlterModelOptions(
            name='productbrand',
            options={'ordering': ('priority', 'id'), 'verbose_name': 'ProductBrand'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ('priority', 'id'), 'verbose_name': 'ProductCategory'},
        ),
        migrations.AlterModelOptions(
            name='productspecs',
            options={'ordering': ('priority', '-id'), 'verbose_name': 'ProductSpecs'},
        ),
        migrations.AddField(
            model_name='productbrand',
            name='brand_code',
            field=models.CharField(default='', max_length=32, unique=True, verbose_name='品牌代码'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='product',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='productattributekey',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='productattributekey',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='productattributekey',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='productattributekey',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='productrelatedattribute',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='productrelatedattribute',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='productrelatedattribute',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='productrelatedattribute',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='productspecs',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='productspecs',
            name='founder',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='productspecs',
            name='last_editor',
            field=models.CharField(blank=True, help_text='username in the User table', max_length=150, null=True, verbose_name='最后修改人'),
        ),
        migrations.AlterField(
            model_name='productspecs',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterUniqueTogether(
            name='productbrand',
            unique_together={('name', 'brand_code')},
        ),
    ]