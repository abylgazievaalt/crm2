# Generated by Django 2.2.4 on 2019-08-13 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190813_0614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='check',
            old_name='orderid',
            new_name='order',
        ),
    ]
