# Generated by Django 2.1.5 on 2019-01-24 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20190124_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
