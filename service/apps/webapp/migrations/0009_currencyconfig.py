# Generated by Django 4.1.7 on 2023-05-11 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_alter_banner_create_at_alter_banner_last_update_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=6, verbose_name='简称')),
                ('mark', models.CharField(max_length=2, verbose_name='货币符号')),
                ('name', models.CharField(max_length=24, verbose_name='货币名称')),
                ('code', models.CharField(max_length=8, verbose_name='货币代码')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.country', verbose_name='国家')),
            ],
            options={
                'db_table': 'currency_config',
            },
        ),
    ]
