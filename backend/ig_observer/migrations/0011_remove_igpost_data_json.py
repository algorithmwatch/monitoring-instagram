# Generated by Django 3.0.2 on 2020-01-31 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0010_auto_20200131_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='igpost',
            name='data_json',
        ),
    ]
