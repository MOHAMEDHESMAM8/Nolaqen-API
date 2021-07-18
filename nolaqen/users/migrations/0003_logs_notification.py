# Generated by Django 3.2.2 on 2021-07-16 16:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0005_alter_courses_photo'),
        ('Groups', '0001_initial'),
        ('users', '0002_auto_20210704_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Accepted Request'), (2, 'Rejected Request'), (3, 'Post'), (4, 'Exam'), (5, 'Lesson')])),
                ('viewed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(db_column='course', on_delete=django.db.models.deletion.CASCADE, to='Courses.courses')),
                ('group', models.ForeignKey(db_column='group', null=True, on_delete=django.db.models.deletion.CASCADE, to='Groups.groups')),
                ('student', models.ForeignKey(db_column='student', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.student')),
                ('teacher', models.ForeignKey(db_column='teacher', on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs_courses', to='Courses.courses')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs_student', to='users.student')),
            ],
        ),
    ]