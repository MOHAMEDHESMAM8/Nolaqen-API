# Generated by Django 3.2.2 on 2021-07-03 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Courses', '0002_student_courses_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(db_column='course', on_delete=django.db.models.deletion.CASCADE, related_name='posts_courses', to='Courses.courses')),
            ],
        ),
    ]