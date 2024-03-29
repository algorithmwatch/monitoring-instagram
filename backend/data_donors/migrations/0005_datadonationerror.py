# Generated by Django 3.0.2 on 2020-01-21 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_donors', '0004_auto_20200117_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDonationError',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True,
                                          max_length=255,
                                          null=True)),
                ('payload', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
