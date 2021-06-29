# Generated by Django 3.0.2 on 2020-01-21 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_observer', '0004_iguser_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='igpost',
            name='ig_type',
            field=models.CharField(choices=[('GraphImage', 'GraphImage'),
                                            ('GraphSidecar', 'GraphSidecar'),
                                            ('GraphVideo', 'GraphVideo')],
                                   max_length=15),
        ),
    ]