# Generated by Django 4.1.7 on 2023-04-21 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_alter_managerdownload_status'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='managerdownload',
            table='manager_download',
        ),
    ]