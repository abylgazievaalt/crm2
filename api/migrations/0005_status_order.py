# Generated by Django 2.2.4 on 2019-08-19 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190816_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Order'),
        ),
    ]
