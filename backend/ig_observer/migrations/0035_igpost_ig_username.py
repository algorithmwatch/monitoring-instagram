# Generated by Django 3.0.11 on 2021-04-14 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0034_auto_20210413_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='igpost',
            name='ig_username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
