# Generated by Django 2.1.5 on 2019-01-31 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]