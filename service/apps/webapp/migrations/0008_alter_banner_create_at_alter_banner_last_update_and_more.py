# Generated by Django 4.1.7 on 2023-04-29 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_chinaprovincearea_parent_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='country',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='country',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
        migrations.AlterField(
            model_name='managerdownload',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='managerdownload',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='最新一次更新'),
        ),
    ]
