# Generated by Django 3.0.11 on 2020-12-04 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0030_iguser_last_scrape'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iguser',
            name='last_scrape',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]