# Generated by Django 2.2.4 on 2019-08-14 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='login',
            new_name='username',
        ),
    ]