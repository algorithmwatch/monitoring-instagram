# Generated by Django 3.0.2 on 2020-01-16 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0001_initial'),
        ('data_donors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('position_in_list',
                 models.IntegerField(
                     help_text='Position in DataDonation ig_posts_seen list')),
                ('data_donation',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='data_donors.DataDonation')),
                ('ig_item',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='ig_observer.IgPost')),
            ],
        ),
    ]
