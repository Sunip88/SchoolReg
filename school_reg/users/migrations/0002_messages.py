# Generated by Django 2.1.5 on 2019-01-22 12:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('send_date', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('send_from', models.ForeignKey(on_delete=models.SET('Deleted'), related_name='user_from', to=settings.AUTH_USER_MODEL)),
                ('send_to', models.ForeignKey(on_delete=models.SET('Deleted'), related_name='user_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]