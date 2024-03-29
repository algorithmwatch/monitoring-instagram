# Generated by Django 3.0.7 on 2020-06-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0022_igpost_ig_media_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iguser',
            name='ig_id',
            field=models.CharField(db_index=True,
                                   max_length=50,
                                   null=True,
                                   unique=True),
        ),
        migrations.AlterField(
            model_name='iguser',
            name='ig_profile_pic',
            field=models.ImageField(null=True, upload_to='profile_pic/'),
        ),
    ]
