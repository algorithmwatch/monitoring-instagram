# Generated by Django 3.0.2 on 2020-02-11 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_donors', '0013_auto_20200211_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='display_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
