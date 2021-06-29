# Generated by Django 3.0.7 on 2020-09-15 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_donors', '0017_auto_20200624_1016'),
        ('ig_observer', '0026_igpost_deleted_by_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgUserFollowedBy',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(null=True)),
                ('created_by',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='data_donors.Donor')),
                ('ig_user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='ig_observer.IgUser')),
            ],
            options={
                'verbose_name': 'Monitored User is followed by',
                'verbose_name_plural': 'Monitored User is followed by',
            },
        ),
    ]