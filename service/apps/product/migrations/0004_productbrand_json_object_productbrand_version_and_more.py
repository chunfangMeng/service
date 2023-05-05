# Generated by Django 4.1.7 on 2023-05-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrand',
            name='json_object',
            field=models.JSONField(null=True, verbose_name='旧版本数据'),
        ),
        migrations.AddField(
            model_name='productbrand',
            name='version',
            field=models.IntegerField(default=0, verbose_name='版本号'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='status',
            field=models.IntegerField(choices=[(0, 'Init'), (1, 'Draft'), (2, 'Online'), (3, 'Deleted'), (4, 'Offline')], default=0, verbose_name='状态'),
        ),
    ]