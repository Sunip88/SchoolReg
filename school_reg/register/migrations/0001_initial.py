# Generated by Django 2.1.1 on 2018-12-31 19:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(blank=True, max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField(choices=[(1, '1'), (1.5, '1+'), (1.75, '2-'), (2, '2'), (2.5, '2+'), (2.75, '3-'), (3, '3'), (3.5, '3+'), (3.75, '4-'), (4, '4'), (4.5, '4+'), (4.75, '5-'), (5, '5'), (5.5, '5+'), (5.75, '6-'), (6, '6')])),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PresenceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('present', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_birth', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(3000)])),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Classes')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('classes', models.ManyToManyField(to='register.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.ManyToManyField(to='register.Subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='presencelist',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Student'),
        ),
        migrations.AddField(
            model_name='parent',
            name='students',
            field=models.ManyToManyField(to='register.Student'),
        ),
        migrations.AddField(
            model_name='parent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grades',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Student'),
        ),
        migrations.AddField(
            model_name='grades',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Subject'),
        ),
        migrations.AddField(
            model_name='classes',
            name='educator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Teacher'),
        ),
    ]