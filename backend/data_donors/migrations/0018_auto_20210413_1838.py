# Generated by Django 3.0.11 on 2021-04-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_donors', '0017_auto_20200624_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='datadonation',
            name='donation_type',
            field=models.CharField(choices=[('FEED', 'Feed'),
                                            ('EXPLORE', 'Explore')],
                                   default='FEED',
                                   max_length=7),
        ),
        migrations.AlterField(
            model_name='datadonation',
            name='ig_posts_seen',
            field=models.IntegerField(null=True),
        ),
    ]