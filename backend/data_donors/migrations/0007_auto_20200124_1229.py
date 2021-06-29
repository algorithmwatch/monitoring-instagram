# Generated by Django 3.0.2 on 2020-01-24 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0005_auto_20200121_1317'),
        ('data_donors', '0006_auto_20200121_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datadonation',
            name='donor_id',
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('ig_donor_id', models.CharField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('following',
                 models.ManyToManyField(related_name='followers',
                                        to='ig_observer.IgUser')),
            ],
        ),
        migrations.AddField(
            model_name='datadonation',
            name='donor',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='data_donors.Donor'),
        ),
    ]