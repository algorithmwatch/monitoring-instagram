# Generated by Django 3.0.11 on 2020-11-24 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0029_auto_20201122_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='iguser',
            name='last_scrape',
            field=models.DateTimeField(null=True),
        ),
    ]
