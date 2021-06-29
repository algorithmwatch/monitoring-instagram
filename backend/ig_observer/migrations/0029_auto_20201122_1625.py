# Generated by Django 3.0.11 on 2020-11-22 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0028_auto_20200918_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iguser',
            name='ig_id',
            field=models.CharField(blank=True,
                                   db_index=True,
                                   max_length=50,
                                   null=True,
                                   unique=True),
        ),
        migrations.AlterField(
            model_name='iguser',
            name='ig_profile_pic',
            field=models.ImageField(blank=True,
                                    null=True,
                                    upload_to='profile_pic/'),
        ),
    ]