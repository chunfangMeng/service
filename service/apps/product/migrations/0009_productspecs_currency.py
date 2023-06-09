# Generated by Django 4.1.7 on 2023-05-11 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_currencyconfig'),
        ('product', '0008_alter_productattributekey_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productspecs',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.currencyconfig', verbose_name='货币'),
        ),
    ]
