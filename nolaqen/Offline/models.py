from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    phone_regex = RegexValidator(regex=r'^(010|011|012|015)',
                                 message="رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم")
    phone = models.CharField(validators=[
        RegexValidator('^(010|011|012|015)[0-9]{8}$',
                       message='رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم',
                       ), ], max_length=11)
    parent_phone = models.CharField(validators=[RegexValidator('^(010|011|012|015)[0-9]{8}$',
                                                               message='رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم', ), ],
                                    max_length=11)

    def __str__(self):
        return self.name


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey("users.Teacher", related_name='courses_teacher_offline', on_delete=models.CASCADE,
                                db_column='teacher')
    name = models.CharField(max_length=50)
    level = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1)
    ])

    def __str__(self):
        return self.name


class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE, db_column='course',related_name='group_courses')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student_courses(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE,db_column='course',related_name='student_courses_courses')
    group = models.ForeignKey("Groups", on_delete=models.CASCADE,db_column='group',related_name='student_courses_groups')
    code = models.CharField(max_length=10)
    student = models.ForeignKey("Students", on_delete=models.CASCADE,db_column='student',related_name='student_courses_students')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'student'],
        unique_together = ['group_id', 'code'],
        indexes = [
            models.Index(fields=['course'], name='IX_Student_courses'),
        ]


class Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE,db_column='course',related_name='sessions_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey("Groups", on_delete=models.CASCADE,db_column='sessions_groups')

    def __str__(self):
        return self.course.name


class Session_data(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey("Students", on_delete=models.CASCADE,db_column='student',related_name='session_data_students')
    session = models.ForeignKey("Sessions", on_delete=models.CASCADE,db_column='session',related_name='session_data_sessions')
    attendance = models.BooleanField(default=False)
    home_work = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)

    class Meta:
        unique_together = ['session', 'student'],
        indexes = [
            models.Index(fields=['session'], name='IX_Session_data_session'),
        ]
