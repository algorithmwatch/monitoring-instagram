# Generated by Django 3.0.2 on 2020-01-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0002_auto_20200117_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='igpost',
            name='ig_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='igpost',
            name='ig_shortcode',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]