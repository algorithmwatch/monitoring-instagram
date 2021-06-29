# Generated by Django 3.0.2 on 2020-01-20 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ig_observer', '0003_auto_20200117_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='iguser',
            name='created_by',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]