# Generated by Django 4.1.7 on 2023-04-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermember',
            name='gender',
            field=models.IntegerField(choices=[[0, 'UNKNOWN'], [1, 'MAN'], [2, 'WOMAN'], [3, 'SECRET']], default=0, help_text='性别'),
        ),
    ]
