# Generated by Django 4.1.7 on 2023-04-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_chinaprovincearea'),
    ]

    operations = [
        migrations.AddField(
            model_name='chinaprovincearea',
            name='parent_code',
            field=models.CharField(blank=True, help_text='父级行政区域代码', max_length=12, null=True),
        ),
    ]
