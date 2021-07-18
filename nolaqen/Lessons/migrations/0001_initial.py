# Generated by Django 3.2.2 on 2021-07-03 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('Courses', '0002_student_courses_group'),
        ('Groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(db_column='course', on_delete=django.db.models.deletion.CASCADE, related_name='lessons_courses', to='Courses.courses')),
            ],
        ),
        migrations.CreateModel(
            name='views',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.BooleanField(default=False)),
                ('single_view', models.PositiveSmallIntegerField(default=6)),
            ],
        ),
        migrations.CreateModel(
            name='Student_lessons',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.ForeignKey(db_column='lesson', on_delete=django.db.models.deletion.CASCADE, related_name='Student_lessons_lessons', to='Lessons.lessons')),
                ('student', models.ForeignKey(db_column='student', on_delete=django.db.models.deletion.CASCADE, related_name='Student_lessons_students', to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson_views',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('views', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(db_column='lesson', on_delete=django.db.models.deletion.CASCADE, related_name='lesson_views_lessons', to='Lessons.lessons')),
                ('student', models.ForeignKey(db_column='student', on_delete=django.db.models.deletion.CASCADE, related_name='lesson_views_students', to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson_groups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.ForeignKey(db_column='group', on_delete=django.db.models.deletion.CASCADE, related_name='lesson_groups_groups', to='Groups.groups')),
                ('lesson', models.ForeignKey(db_column='lesson', on_delete=django.db.models.deletion.CASCADE, related_name='lesson_groups_lessons', to='Lessons.lessons')),
            ],
        ),
        migrations.AddIndex(
            model_name='student_lessons',
            index=models.Index(fields=['student'], name='IX_Student_lessons'),
        ),
        migrations.AlterUniqueTogether(
            name='student_lessons',
            unique_together={('lesson', 'student')},
        ),
        migrations.AddIndex(
            model_name='lessons',
            index=models.Index(fields=['course'], name='IX_lessons'),
        ),
        migrations.AddIndex(
            model_name='lesson_views',
            index=models.Index(fields=['lesson', 'student'], name='IX_Lesson_views'),
        ),
        migrations.AlterUniqueTogether(
            name='lesson_views',
            unique_together={('lesson', 'student')},
        ),
        migrations.AddIndex(
            model_name='lesson_groups',
            index=models.Index(fields=['group'], name='IX_Lesson_groups'),
        ),
        migrations.AlterUniqueTogether(
            name='lesson_groups',
            unique_together={('lesson', 'group')},
        ),
    ]
