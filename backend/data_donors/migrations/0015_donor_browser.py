# Generated by Django 3.0.5 on 2020-05-05 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_donors', '0014_donor_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='browser',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
