# Generated by Django 4.1.7 on 2023-05-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_userloginlog_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manageruser',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Unknown'), (1, 'Man'), (2, 'Woman'), (3, 'Secret')], default=0, help_text='性别'),
        ),
    ]
