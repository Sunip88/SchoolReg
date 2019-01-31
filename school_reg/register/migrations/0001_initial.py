# Generated by Django 2.1.5 on 2019-01-31 17:19

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
            name='Adverts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=64)),
                ('date', models.DateField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertsClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=64)),
                ('date', models.DateField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(blank=True, max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_set', models.DateField(auto_now_add=True)),
                ('date_of_event', models.DateField()),
                ('title', models.CharField(max_length=64)),
                ('text', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GradeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField(choices=[(1, '1'), (1.5, '1+'), (1.75, '2-'), (2, '2'), (2.5, '2+'), (2.75, '3-'), (3, '3'), (3.5, '3+'), (3.75, '4-'), (4, '4'), (4.5, '4+'), (4.75, '5-'), (5, '5'), (5.5, '5+'), (5.75, '6-'), (6, '6')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.GradeCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('accepted', models.NullBooleanField()),
                ('re_text', models.CharField(default='', max_length=256)),
                ('date', models.DateField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
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
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek')])),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Classes')),
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
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr', models.IntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='hours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.WorkingHours'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.ClassRoom'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Subject'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Teacher'),
        ),
        migrations.AddField(
            model_name='presencelist',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Student'),
        ),
        migrations.AddField(
            model_name='presencelist',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Schedule'),
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
            model_name='notice',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Teacher'),
        ),
        migrations.AddField(
            model_name='notice',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Student'),
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
            model_name='event',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Schedule'),
        ),
        migrations.AddField(
            model_name='classes',
            name='educator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Teacher'),
        ),
        migrations.AddField(
            model_name='advertsclass',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Teacher'),
        ),
        migrations.AddField(
            model_name='advertsclass',
            name='classes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Classes'),
        ),
    ]
