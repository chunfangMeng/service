# Generated by Django 4.1.7 on 2023-05-11 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('priority', '-id'), 'verbose_name': 'Product'},
        ),
    ]
