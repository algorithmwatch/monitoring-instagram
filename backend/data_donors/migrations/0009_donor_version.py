# Generated by Django 3.0.2 on 2020-01-27 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_donors', '0008_auto_20200124_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='version',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
