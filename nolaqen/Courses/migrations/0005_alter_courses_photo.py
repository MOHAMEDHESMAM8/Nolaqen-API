# Generated by Django 3.2.2 on 2021-07-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0004_student_courses_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='courses/%y/%m/%d'),
        ),
    ]
